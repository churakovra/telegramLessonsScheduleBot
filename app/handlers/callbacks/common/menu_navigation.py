from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.handlers.commands.menu import markup_type_by_role
from app.keyboard.builder import MarkupBuilder
from app.keyboard.callback_factories.menu import MenuCallback
from app.schemas.user_dto import UserDTO
from app.utils import message_template
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import KeyboardType
from app.utils.enums.menu_type import MenuType
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

main_menus = [MenuType.TEACHER, MenuType.STUDENT, MenuType.ADMIN]


@router.callback_query(MenuCallback.filter(F.menu_type.in_(markup_type_by_menu_type)))
async def handle_teacher_menu(
    callback: CallbackQuery, callback_data: MenuCallback
) -> None:
    menu_type = callback_data.menu_type
    markup = MarkupBuilder.build(markup_type_by_menu_type[menu_type])
    message_text = (
        BotStrings.Common.MENU
        if menu_type in main_menus
        else BotStrings.Common.SUB_MENU
    )
    await callback.message.answer(text=message_text, reply_markup=markup)
    await callback.answer()


@router.callback_query(MenuCallback.filter(F.menu_type == MenuType.CANCEL))
async def handle_cancel(
    callback: CallbackQuery,
    state: FSMContext,
    user: UserDTO,
):
    markup = MarkupBuilder.build(markup_type_by_role[user.role])
    reply_message = message_template.main_menu_message(markup)
    await state.clear()
    await callback.message.answer(**reply_message)
    await callback.answer()
