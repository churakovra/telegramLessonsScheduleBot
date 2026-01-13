from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.lesson_service import LessonService
from app.services.teacher_service import TeacherService
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import KeyboardType
from app.utils.enums.menu_type import MenuType
from app.utils.exceptions.lesson_exceptions import LessonsNotFoundException
from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.utils.keyboard.callback_factories.lessons import LessonDelete
from app.utils.keyboard.callback_factories.menu import MenuCallback
from app.utils.keyboard.builder import MarkupBuilder
from app.utils.keyboard.context import ConfirmDeletionKeyboardContext, LessonOperationKeyboardContext
from app.utils.logger import setup_logger
from app.utils import message_template as mt

router = Router()
logger = setup_logger(__name__)


@router.callback_query(MenuCallback.filter(F.menu_type == MenuType.TEACHER_LESSON_DELETE))
async def on_delete_button_pressed(
    callback: CallbackQuery,
    session: AsyncSession,
):
    teacher_service = TeacherService(session)
    lesson_service = LessonService(session)
    try:
        message_text = ""
        markup = None
        teacher_username = callback.from_user.username
        teacher = await teacher_service.get_teacher(teacher_username)
        lessons = await lesson_service.get_teacher_lessons(teacher.uuid)
        message_text = BotStrings.Teacher.TEACHER_LESSON_DELETE
        markup_context = LessonOperationKeyboardContext(lessons, LessonDelete)
        markup = MarkupBuilder.build(KeyboardType.LESSONS_OPERATION, markup_context)
    except UserNotFoundException as e:
        logger.error(e.message)
        message_text = BotStrings.User.USER_INFO_ERROR
        return
    except LessonsNotFoundException as e:
        logger.error(e.message)
        message_text = BotStrings.Teacher.TEACHER_LESSONS_WERE_NOT_FOUND
    await callback.message.answer(text=message_text, reply_markup=markup)
    await callback.answer()


@router.callback_query(LessonDelete.filter(F.confirmed == False))
async def request_delete_confirmation(
    callback: CallbackQuery, callback_data: LessonDelete
):
    markup_context = ConfirmDeletionKeyboardContext(LessonDelete, callback_data)
    markup = MarkupBuilder.build(KeyboardType.CONFIRM_DELETION, markup_context)
    await callback.message.answer(**mt.confirm_lesson_deletion(markup))
    await callback.answer()


@router.callback_query(LessonDelete.filter(F.confirmed == True))
async def delete_lesson(
    callback: CallbackQuery, callback_data: LessonDelete, session: AsyncSession
):
    lesson_service = LessonService(session)
    await lesson_service.detach_lesson(callback_data.uuid)
    await lesson_service.delete_lesson(callback_data.uuid)
    await callback.message.answer(**mt.lesson_deletion_success)
    await callback.answer()