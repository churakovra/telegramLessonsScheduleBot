import aiogram.types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from datetime_utils import weekdays
from strings import Strings as str


def get_set_types_markup() -> InlineKeyboardMarkup:
    days_bt = InlineKeyboardButton(text=str.BRANCH_DAYS, callback_data=str.CALLBACK_BRANCH_DAYS)
    manual_bt = InlineKeyboardButton(text=str.BRANCH_MANUAL, callback_data=str.CALLBACK_BRANCH_MANUAL)
    markup = InlineKeyboardMarkup(inline_keyboard=[[days_bt, manual_bt]])
    return markup


def get_weekdays_markup() -> InlineKeyboardMarkup:
    keyboard_rows = []
    for items in weekdays.items():
        button = aiogram.types.InlineKeyboardButton(text=items[1], callback_data=f'day_{items[0]}')
        keyboard_rows.append([button])
    markup = aiogram.types.InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    return markup