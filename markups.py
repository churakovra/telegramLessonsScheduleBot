from datetime import datetime

import aiogram.types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from datetime_utils import weekdays, which_day
from strings import Strings as str


def get_set_types_markup() -> InlineKeyboardMarkup:
    days_bt = InlineKeyboardButton(text=str.BRANCH_DAYS, callback_data=str.CALLBACK_BRANCH_DAYS)
    manual_bt = InlineKeyboardButton(text=str.BRANCH_MANUAL, callback_data=str.CALLBACK_BRANCH_MANUAL)
    markup = InlineKeyboardMarkup(inline_keyboard=[[days_bt, manual_bt]])
    return markup


def get_weekdays_markup(cday: datetime) -> InlineKeyboardMarkup:
    ccal = 0 if which_day(cday) > 4 else which_day(cday)
    k = list(weekdays.keys())
    v = list(weekdays.values())
    keyboard_rows = []
    for i in range(ccal, len(weekdays)):
        button = aiogram.types.InlineKeyboardButton(text=v[i], callback_data=f'day_{k[i]}')
        keyboard_rows.append([button])
    markup = aiogram.types.InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    return markup
