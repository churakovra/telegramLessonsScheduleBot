from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboard.builder import MarkupBuilder
from app.keyboard.callback_factories.lesson import (
    LessonCreateCallback,
    LessonDeleteCallback,
    LessonInfoCallback,
    LessonListCallback,
    LessonUpdateCallback,
)
from app.keyboard.context import (
    ConfirmDeletionKeyboardContext,
    EntitiesListKeyboardContext,
    EntityOperationsKeyboardContext,
    SpecsToUpdateKeyboardContext,
)
from app.services.lesson_service import LessonService
from app.services.teacher_service import TeacherService
from app.states.schedule_states import ScheduleStates
from app.utils import message_template as mt
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import ActionType, EntityType, KeyboardType
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
        markup = MarkupBuilder.build(KeyboardType.CANCEL)
        message = await callback.message.answer(
            text=BotStrings.Teacher.TEACHER_LESSON_ADD_LABEL, reply_markup=markup
        )
        await state.update_data(previous_message_id=message.message_id)
    except UserNotFoundException:
        logger.error(
            f"Teacher {teacher.uuid} tried to add new lesson, but didn't have enough rights"
        )
        await callback.message.answer(BotStrings.Teacher.NOT_ENOUGH_RIGHTS)
        return
    finally:
        await callback.answer()


@router.callback_query(LessonListCallback.filter())
async def list(callback: CallbackQuery, session: AsyncSession):
    teacher_service = TeacherService(session)
    lesson_service = LessonService(session)
    try:
        markup = None
        teacher_username = callback.from_user.username
        teacher = await teacher_service.get_teacher(teacher_username)
        lessons = await lesson_service.get_teacher_lessons(teacher.uuid)
        message_text = BotStrings.Teacher.TEACHER_LESSON_LIST
        markup_context = EntitiesListKeyboardContext(lessons, EntityType.LESSON)
        markup = MarkupBuilder.build(KeyboardType.ENTITIES_LIST, markup_context)
    except UserNotFoundException as e:
        logger.error(e.message)
        message_text = BotStrings.User.USER_INFO_ERROR
        return
    except LessonsNotFoundException as e:
        logger.error(e.message)
        message_text = BotStrings.Teacher.TEACHER_LESSONS_WERE_NOT_FOUND
    await callback.message.answer(text=message_text, reply_markup=markup)
    await callback.answer()


@router.callback_query(LessonInfoCallback.filter())
async def get_lesson_info(
    callback: CallbackQuery, callback_data: LessonInfoCallback, session: AsyncSession
):
    lesson_service = LessonService(session)
    lesson = await lesson_service.get_lesson(callback_data.uuid)
    response_msg = await lesson_service.get_lesson_info(lesson)
    markup_context = EntityOperationsKeyboardContext(lesson.uuid, EntityType.LESSON)
    markup = MarkupBuilder.build(KeyboardType.ENTITY_OPERATIONS, markup_context)
    await callback.message.answer(
        text=response_msg, parse_mode="MarkdownV2", reply_markup=markup
    )
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
    markup_context = SpecsToUpdateKeyboardContext(
        lesson_uuid=callback_data.uuid,
        specs=lesson_specs,
        callback_data_cls=LessonUpdateCallback,
    )
    markup = MarkupBuilder.build(KeyboardType.SPECS_TO_UPDATE, markup_context)
    text = BotStrings.Teacher.TEACHER_LESSON_UPDATE_SELECT_SPEC
    await callback.message.answer(text=text, reply_markup=markup)
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
    await callback.message.answer(spec_to_message[callback_data.spec])
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
    message = await callback.message.answer(BotStrings.Teacher.TEACHER_LESSON_ADD_LABEL)
    await state.update_data(previous_message_id=message.message_id)
    await callback.answer()


@router.callback_query(LessonDeleteCallback.filter(not F.confirmed))
async def request_delete_confirmation(
    callback: CallbackQuery, callback_data: LessonDeleteCallback
):
    markup_context = ConfirmDeletionKeyboardContext(LessonDeleteCallback, callback_data)
    markup = MarkupBuilder.build(KeyboardType.CONFIRM_DELETION, markup_context)
    await callback.message.answer(**mt.confirm_lesson_deletion(markup))
    await callback.answer()


@router.callback_query(LessonDeleteCallback.filter(F.confirmed))
async def delete_lesson(
    callback: CallbackQuery, callback_data: LessonDeleteCallback, session: AsyncSession
):
    lesson_service = LessonService(session)
    await lesson_service.detach_lesson(callback_data.uuid)
    await lesson_service.delete_lesson(callback_data.uuid)
    await callback.message.answer(**mt.lesson_deletion_success())
    await callback.answer()
