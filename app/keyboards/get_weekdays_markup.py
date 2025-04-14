from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.utils.datetime_utils import weekdays, which_day


def get_weekdays(cday: datetime) -> InlineKeyboardMarkup:
    ccal = 0 if which_day(cday) > 4 else which_day(cday)
    k = list(weekdays.keys())
    v = list(weekdays.values())
    keyboard_rows = []
    for i in range(ccal, len(weekdays)):
        button = InlineKeyboardButton(text=v[i], callback_data=f'day_{k[i]}')
        keyboard_rows.append([button])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    return markup
