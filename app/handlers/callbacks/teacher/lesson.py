from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboard.callback_factories.lesson import (
    LessonCreateCallback,
    LessonDeleteCallback,
    LessonInfoCallback,
    LessonListCallback,
    LessonUpdateCallback,
)
from app.keyboard.fabric import (
    cancel_markup,
    confirm_deletion,
    lesson_buttons,
    specs_to_update,
    teacher_main_menu,
)
from app.message.models import BotMessage
from app.message.utils import get_lesson_info
from app.schemas.user import UserDTO
from app.services.lesson_service import LessonService
from app.services.teacher_service import TeacherService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import ActionType, EntityType, UserRole
from app.utils.exceptions.lesson_exceptions import LessonsNotFoundException
from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.utils.logger import setup_logger

router = Router()


logger = setup_logger(__name__)


@router.callback_query(LessonCreateCallback.filter())
async def create(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext
) -> None:
    teacher_service = TeacherService(session)
    try:
        teacher = await teacher_service.get_teacher(callback.from_user.username)
        await state.update_data(uuid_teacher=teacher.uuid)
        await state.update_data(operation_type=ActionType.CREATE)
        await state.set_state(ScheduleStates.wait_for_teacher_lesson_label)
        await callback.message.delete()

        markup = cancel_markup()
        message = BotMessage(
            text=BotStrings.Teacher.TEACHER_LESSON_ADD_LABEL, markup=markup
        )
        sent_message = await callback.message.answer(**message.to_aiogram_kwargs())
        await state.update_data(previous_message_id=sent_message.message_id)
    except UserNotFoundException:
        logger.error(f"Teacher tried to add new lesson, but didn't have enough rights")
        await callback.message.answer(BotStrings.Teacher.NOT_ENOUGH_RIGHTS)
        return
    finally:
        await callback.answer()


@router.callback_query(LessonListCallback.filter())
async def list_lessons(callback: CallbackQuery, session: AsyncSession, user: UserDTO):
    lesson_service = LessonService(session)
    try:
        lessons = await lesson_service.get_teacher_lessons(user.uuid)
        markup = lesson_buttons(type("Context", (), {"lessons": lessons})())
        message = BotMessage(text=BotStrings.Teacher.TEACHER_LESSON_LIST, markup=markup)
    except LessonsNotFoundException as e:
        logger.error(e.message)
        markup = teacher_main_menu()
        message = BotMessage(
            text=BotStrings.Teacher.TEACHER_LESSONS_WERE_NOT_FOUND, markup=markup
        )
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()


@router.callback_query(LessonInfoCallback.filter())
async def info(
    callback: CallbackQuery, callback_data: LessonInfoCallback, session: AsyncSession
):
    lesson_service = LessonService(session)
    lesson = await lesson_service.get_lesson(callback_data.uuid)
    text = get_lesson_info(lesson)
    from app.keyboard.fabric import entity_operations

    markup = entity_operations(lesson.uuid, type(lesson))
    message = BotMessage(text=text, markup=markup)
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()


@router.callback_query(LessonUpdateCallback.filter(F.spec.is_(None)))
async def select_spec(
    callback: CallbackQuery, callback_data: LessonUpdateCallback
) -> None:
    lesson_specs = {
        "label": "Название",  # TODO mv spec key in enum or smth
        "duration": "Продолжительность",
        "price": "Цена",
    }

    markup = specs_to_update(
        type(
            "Context",
            (),
            {
                "lesson_uuid": callback_data.uuid,
                "specs": lesson_specs,
                "callback_data_cls": LessonUpdateCallback,
            },
        )()
    )
    message = BotMessage(
        text=BotStrings.Teacher.TEACHER_LESSON_UPDATE_SELECT_SPEC, markup=markup
    )
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()


@router.callback_query(
    LessonUpdateCallback.filter(F.spec.in_(["label", "duration", "price"]))
)
async def update_lesson_by_spec(
    callback: CallbackQuery, callback_data: LessonUpdateCallback, state: FSMContext
) -> None:
    spec_to_message = {
        "label": BotStrings.Teacher.TEACHER_LESSON_ADD_LABEL,
        "duration": BotStrings.Teacher.TEACHER_LESSON_ADD_DURATION,
        "price": BotStrings.Teacher.TEACHER_LESSON_ADD_PRICE,
        None: "Ooops",  # TODO refactor this
    }
    await state.update_data(lesson_uuid=callback_data.uuid, spec=callback_data.spec)
    await state.set_state(ScheduleStates.wait_for_lesson_update)
    message = BotMessage(text=spec_to_message[callback_data.spec])
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()


@router.callback_query(LessonUpdateCallback.filter(F.spec == "all"))
async def update_whole_lesson(
    callback: CallbackQuery,
    callback_data: LessonUpdateCallback,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    teacher_service = TeacherService(session)
    teacher = await teacher_service.get_teacher(callback.from_user.username)
    await state.update_data(uuid_teacher=teacher.uuid)
    await state.update_data(uuid_lesson=callback_data.uuid)
    await state.update_data(operation_type=ActionType.UPDATE)
    await state.set_state(ScheduleStates.wait_for_teacher_lesson_label)

    markup = cancel_markup()
    message = BotMessage(
        text=BotStrings.Teacher.TEACHER_LESSON_ADD_LABEL, markup=markup
    )
    sent_message = await callback.message.answer(**message.to_aiogram_kwargs())
    await state.update_data(previous_message_id=sent_message.message_id)
    await callback.answer()


@router.callback_query(LessonDeleteCallback.filter(not F.confirmed))
async def request_delete_confirmation(
    callback: CallbackQuery, callback_data: LessonDeleteCallback
):
    markup = confirm_deletion(
        type(
            "Context",
            (),
            {"callback_data_cls": LessonDeleteCallback, "callback_data": callback_data},
        )()
    )
    message = BotMessage(
        text=BotStrings.Teacher.TEACHER_LESSON_DELETE_CONFIRMATION_REQUEST,
        markup=markup,
    )
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()


@router.callback_query(LessonDeleteCallback.filter(F.confirmed))
async def delete_lesson(
    callback: CallbackQuery, callback_data: LessonDeleteCallback, session: AsyncSession
):
    lesson_service = LessonService(session)
    await lesson_service.detach_lesson(callback_data.uuid)
    await lesson_service.delete_lesson(callback_data.uuid)

    markup = teacher_main_menu()
    message = BotMessage(
        text=BotStrings.Teacher.TEACHER_LESSON_DELETE_SUCCESS, markup=markup
    )
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()
