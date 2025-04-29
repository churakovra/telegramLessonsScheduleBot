from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_is_slots_correct_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Да",
            callback_data="slots_correct"
        ),
        InlineKeyboardButton(
            text="Нет",
            callback_data="slots_incorrect"
        )
    )
    return builder.as_markup()