from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.utils.bot_strings import BotStrings


def get_choose_days_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=BotStrings.BRANCH_DAYS,
            callback_data=BotStrings.CALLBACK_BRANCH_DAYS
        )
    )
    return builder.as_markup()
