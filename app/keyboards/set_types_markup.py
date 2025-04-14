from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.utils.strings import Strings as strings


def get_set_types_markup() -> InlineKeyboardMarkup:
    days_bt = InlineKeyboardButton(text=strings.BRANCH_DAYS, callback_data=strings.CALLBACK_BRANCH_DAYS)
    manual_bt = InlineKeyboardButton(text=strings.BRANCH_MANUAL, callback_data=strings.CALLBACK_BRANCH_MANUAL)
    markup = InlineKeyboardMarkup(inline_keyboard=[[days_bt, manual_bt]])
    return markup
