from datetime import datetime
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from gap import Gap
from lesson import Lesson
from schedule import Schedule
from strings import Strings as s

import datetime_utils
import datetime_utils as dt
import markups
import schedule_db


async def send_select_day_message(callback: CallbackQuery):
    message_text = s.WEEKDAY
    weekdays_markup = markups.get_weekdays_markup(callback.message.date)
    await callback.message.edit_text(text=message_text, reply_markup=weekdays_markup)
    await callback.answer()


async def send_set_manual_message(callback: CallbackQuery):
    message_text = s.SET_MANUAL
    await callback.message.edit_text(text=message_text)
    await callback.answer()


async def send_day_schedule(callback: CallbackQuery):
    weekday: int = int(callback.data[len(callback.data) - 1])
    day: datetime = dt.get_datetime_from_weekday(weekday, callback.message.date)
    schedule = Schedule(day)
    keyboard_rows = []
    for gap in schedule.get_schedule():
        dt_s = gap.datetime_start.strftime(datetime_utils.full_format_no_sec)
        dt_e = gap.datetime_end.strftime(datetime_utils.full_format_no_sec)
        text = f'{dt_s} - {dt_e}'
        button = InlineKeyboardButton(
            text=text,
            callbacks=f'gap_{dt_s}'
        )
        keyboard_rows.append([button])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    await callback.message.edit_text(text='Я ебал это собирать', reply_markup=markup)
    await callback.answer()

    def get_schedule(lessons: list[Lesson]) -> list[datetime]:
        pass


def get_day_lessons(day: datetime) -> list[Lesson]:
    lessons = schedule_db.get_lessons(day)
    return lessons
