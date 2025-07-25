from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.utils.bot_strings import BotStrings


def get_is_slots_correct_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=BotStrings.YES,
        callback_data=BotStrings.CALLBACK_SLOTS_CORRECT
    )
    builder.button(
        text=BotStrings.NO,
        callback_data=BotStrings.CALLBACK_SLOTS_INCORRECT
    )

    return builder.as_markup()
