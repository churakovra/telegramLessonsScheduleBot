from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.utils.config.logger import setup_logger
from app.utils.enums.bot_values import UserRoles
from app.utils.exceptions.user_exceptions import UserUnknownRoleException
from app.utils.bot_strings import bot_strings as bt

logger = setup_logger()


class MainMenuCallback(CallbackData, prefix="fab-main-menu"):
    menu_type: str


def get_main_menu_markup(role: UserRoles) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if role == UserRoles.TEACHER:
        callbacks = {
            "Ученики": bt.CALLBACK_GROUP_TEACHER_STUDENT,
            "Окошки": bt.CALLBACK_GROUP_TEACHER_SLOT,
            "Уроки": bt.CALLBACK_GROUP_TEACHER_LESSON
        }
    elif role == UserRoles.STUDENT:
        callbacks = {
            "Запланированные уроки": bt.CALLBACK_GROUP_STUDENT_SLOT_LIST,
        }
    else:
        raise UserUnknownRoleException(None, role)
    for name, value in callbacks.items():
        builder.button(
            text=name,
            callback_data=MainMenuCallback(menu_type=value)
        )
        logger.debug(f"get_menu_markup: name={name}; callback_data={value}")
    builder.adjust(1)
    return builder.as_markup()
