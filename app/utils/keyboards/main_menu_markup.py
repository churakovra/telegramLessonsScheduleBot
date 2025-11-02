from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.schemas.user_dto import UserDTO
from app.config.logger import setup_logger
from app.utils.enums.bot_values import UserRole
from app.utils.exceptions.user_exceptions import UserUnknownRoleException
from app.utils.keyboards.menu_data.main_menu_admin import MainMenuDataAdmin
from app.utils.keyboards.menu_data.main_menu_student import MainMenuDataStudent
from app.utils.keyboards.menu_data.main_menu_teacher import MainMenuDataTeacher

logger = setup_logger()


def get_main_menu_markup(role: UserRole) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    match role:
        case UserRole.TEACHER:
            menu_data = MainMenuDataTeacher.teacher_menu
        case UserRole.STUDENT:
            menu_data = MainMenuDataStudent.student_menu
        case UserRole.ADMIN:
            menu_data = MainMenuDataAdmin.admin_menu
        case _:
            raise UserUnknownRoleException(role=role)

    for menu in menu_data:
        builder.button(text=menu.text, callback_data=menu.callback_data)
        logger.debug(f"get_menu_markup: name={menu.text}; callback_data={menu.callback_data}")

    builder.adjust(1)
    return builder.as_markup()
