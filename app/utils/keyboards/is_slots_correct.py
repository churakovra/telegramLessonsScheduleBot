from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.utils.bot_strings import BotStrings


def get_is_slots_correct_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=BotStrings.Menu.YES,
        callback_data=BotStrings.Teacher.CALLBACK_SLOTS_CORRECT
    )
    builder.button(
        text=BotStrings.Menu.NO,
        callback_data=BotStrings.Teacher.CALLBACK_SLOTS_INCORRECT
    )

    return builder.as_markup()
