from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.lesson_service import LessonService
from app.services.teacher_service import TeacherService
from app.utils.enums.menu_type import MenuType
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
        teacher_username = callback.from_user.username
        teacher = await teacher_service.get_teacher(teacher_username)
        lessons = await lesson_service.get_teacher_lessons(teacher.uuid)
        markup = MarkupBuilder.delete_lessons_markup(lessons)
    except Exception:
        pass    


@router.callback_query(LessonDelete.filter())
async def delete_lesson(callback: CallbackQuery, session: AsyncSession): ...