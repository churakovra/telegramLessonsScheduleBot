from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.utils.bot_strings import bot_strings as bt


def get_is_slots_correct_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=bt.YES,
        callback_data=bt.CALLBACK_SLOTS_CORRECT
    )
    builder.button(
        text=bt.NO,
        callback_data=bt.CALLBACK_SLOTS_INCORRECT
    )

    return builder.as_markup()
