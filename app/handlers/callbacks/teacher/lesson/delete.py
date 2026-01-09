from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.lesson_service import LessonService
from app.services.teacher_service import TeacherService
from app.utils.bot_strings import BotStrings
from app.utils.enums.menu_type import MenuType
from app.utils.exceptions.lesson_exceptions import LessonsNotFoundException
from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.utils.keyboards.callback_factories.lessons import LessonDelete
from app.utils.keyboards.callback_factories.menu import SubMenu
from app.utils.keyboards.markup_builder import MarkupBuilder
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.callback_query(SubMenu.filter(F.menu_type == MenuType.TEACHER_LESSON_DELETE))
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
        markup = MarkupBuilder.lessons_markup(lessons, LessonDelete)
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
    markup = MarkupBuilder.confirm_deletion_markup(LessonDelete, callback_data)
    await callback.message.answer(
        text=BotStrings.Teacher.TEACHER_LESSON_DELETE_CONFIRMATION_REQUEST,
        reply_markup=markup,
    )
    await callback.answer()


@router.callback_query(LessonDelete.filter(F.confirmed == True))
async def delete_lesson(
    callback: CallbackQuery, callback_data: LessonDelete, session: AsyncSession
):
    lesson_service = LessonService(session)
    await lesson_service.detach_lesson(callback_data.uuid)
    await lesson_service.delete_lesson(callback_data.uuid)
    await callback.message.answer(BotStrings.Teacher.TEACHER_LESSON_DELETE_SUCCESS)
    await callback.answer()