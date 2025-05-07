from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.utils.bot_strings import bot_strings as bt


def get_menu_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=bt.USER_INFO,
            callback_data=bt.CALLBACK_USER_INFO
        )
    )
    return builder.as_markup()
