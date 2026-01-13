from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.lesson_service import LessonService
from app.services.teacher_service import TeacherService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import KeyboardType, OperationType
from app.utils.enums.menu_type import MenuType
from app.utils.exceptions.lesson_exceptions import LessonsNotFoundException
from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.utils.keyboard.callback_factories.lessons import LessonUpdate
from app.utils.keyboard.callback_factories.menu import MenuCallback
from app.utils.keyboard.builder import MarkupBuilder
from app.utils.keyboard.context import LessonOperationKeyboardContext, SpecsToUpdateKeyboardContext
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.callback_query(MenuCallback.filter(F.menu_type == MenuType.TEACHER_LESSON_UPDATE))
async def on_update_button_pressed(callback: CallbackQuery, session: AsyncSession) -> None:
    teacher_service = TeacherService(session)
    lesson_service = LessonService(session)
    try:
        message_text = ""
        markup = None
        teacher_username = callback.from_user.username
        teacher = await teacher_service.get_teacher(teacher_username)
        lessons = await lesson_service.get_teacher_lessons(teacher.uuid)
        message_text = BotStrings.Teacher.TEACHER_LESSON_UPDATE
        markup_context = LessonOperationKeyboardContext(lessons, LessonUpdate)
        markup = MarkupBuilder.build(KeyboardType.LESSONS_OPERATION,markup_context)
    except UserNotFoundException as e:
        logger.error(e.message)
        message_text = BotStrings.User.USER_INFO_ERROR
        return
    except LessonsNotFoundException as e:
        logger.error(e.message)
        message_text = BotStrings.Teacher.TEACHER_LESSONS_WERE_NOT_FOUND
    await callback.message.answer(text=message_text, reply_markup=markup)
    await callback.answer()


@router.callback_query(LessonUpdate.filter(F.spec == None))
async def on_lesson_button_pressed(
    callback: CallbackQuery, callback_data: LessonUpdate
) -> None:
    lesson_specs = {
        "label": "Название",  # TODO mv spec key in enum or smth
        "duration": "Продолжительность",
        "price": "Цена",
    }
    markup_context = SpecsToUpdateKeyboardContext(
        lesson_uuid=callback_data.uuid,
        specs=lesson_specs,
        callback_data_cls=LessonUpdate,
    
    )
    markup = MarkupBuilder.build(KeyboardType.SPECS_TO_UPDATE, markup_context)
    text = BotStrings.Teacher.TEACHER_LESSON_UPDATE_SELECT_SPEC
    await callback.message.answer(text=text, reply_markup=markup)
    await callback.answer()


@router.callback_query(LessonUpdate.filter(F.spec.in_(["label", "duration", "price"])))
async def update_lesson_label(
    callback: CallbackQuery, callback_data: LessonUpdate, state: FSMContext
) -> None:
    spec_to_message = {
        "label": BotStrings.Teacher.TEACHER_LESSON_ADD_LABEL,
        "duration": BotStrings.Teacher.TEACHER_LESSON_ADD_DURATION,
        "price": BotStrings.Teacher.TEACHER_LESSON_ADD_PRICE,
        None: "Ooops" #TODO refactor this
    }
    await state.update_data(lesson_uuid=callback_data.uuid, spec=callback_data.spec)
    await state.set_state(ScheduleStates.wait_for_lesson_update)
    await callback.message.answer(spec_to_message[callback_data.spec])
    await callback.answer()


@router.callback_query(LessonUpdate.filter(F.spec=="all"))
async def update_lesson(
    callback: CallbackQuery, callback_data: LessonUpdate, state: FSMContext, session: AsyncSession
) -> None:
    teacher_service = TeacherService(session)
    teacher = await teacher_service.get_teacher(callback.from_user.username)
    await state.update_data(uuid_teacher=teacher.uuid)
    await state.update_data(uuid_lesson=callback_data.uuid)
    await state.update_data(operation_type=OperationType.UPDATE)
    await state.set_state(ScheduleStates.wait_for_teacher_lesson_label)
    message = await callback.message.answer(BotStrings.Teacher.TEACHER_LESSON_ADD_LABEL)
    await state.update_data(previous_message_id=message.message_id)
    await callback.answer()
