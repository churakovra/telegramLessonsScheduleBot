from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.utils.enums.bot_values import KeyboardType
from app.utils.enums.menu_type import MenuType
from app.utils.keyboard.builder import MarkupBuilder
from app.utils.keyboard.callback_factories.menu import MenuCallback
from app.utils.logger import setup_logger

router = Router()

logger = setup_logger(__name__)


markup_type_by_menu_type = {
    MenuType.TEACHER: KeyboardType.TEACHER_MAIN,
    MenuType.STUDENT: KeyboardType.STUDENT_MAIN,
    MenuType.ADMIN: KeyboardType.ADMIN_MAIN,
    MenuType.TEACHER_STUDENT: KeyboardType.TEACHER_SUB_STUDENT,
    MenuType.TEACHER_SLOT: KeyboardType.TEACHER_SUB_SLOT,
    MenuType.TEACHER_LESSON: KeyboardType.TEACHER_SUB_LESSON,
    MenuType.STUDENT_SLOT: KeyboardType.STUDENT_SUB_SLOT,
    MenuType.STUDENT_TEACHER: KeyboardType.STUDENT_SUB_TEACHER,
    MenuType.ADMIN_TEMP: KeyboardType.ADMIN_SUB_TEMP,
}


@router.callback_query(MenuCallback.filter(F.menu_type.in_(markup_type_by_menu_type)))
async def handle_teacher_menu(
    callback: CallbackQuery, callback_data: MenuCallback
) -> None:
    markup = MarkupBuilder.build(markup_type_by_menu_type[callback_data.menu_type])
    await callback.message.answer(text="Select", reply_markup=markup)
    await callback.answer()
