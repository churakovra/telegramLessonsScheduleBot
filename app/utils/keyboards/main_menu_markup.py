from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.schemas.user_dto import UserDTO
from app.utils.config.logger import setup_logger
from app.utils.enums.bot_values import UserRoles
from app.utils.exceptions.user_exceptions import UserUnknownRoleException
from app.utils.keyboards.callback_factories.main_menu import MainMenuCallback, teacher_menu, student_menu

logger = setup_logger()


def get_main_menu_markup(user: UserDTO) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if user.is_teacher:
        menu_data = teacher_menu
    elif user.is_student:
        menu_data = student_menu
    else:
        raise UserUnknownRoleException(username=user.username, role=None)

    for name, value in menu_data.items():
        builder.button(text=name, callback_data=MainMenuCallback(menu_type=value))
        logger.debug(f"get_menu_markup: name={name}; callback_data={value}")

    builder.adjust(1)
    return builder.as_markup()
