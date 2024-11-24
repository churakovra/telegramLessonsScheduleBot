from datetime import datetime
from strings import Strings as s
from aiogram.types import CallbackQuery
from lesson import Lesson

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


def get_day_schedule(day_callback: str, cday: datetime):
    weekday: int = int(day_callback[len(day_callback) - 1])
    day: datetime = dt.get_datetime_from_weekday(weekday, cday)
    lessons = get_day_lessons(day)
    schedule = get_schedule(lessons)


def get_schedule(lessons: list[Lesson]) -> list[datetime]:
    pass


def get_day_lessons(day: datetime) -> list[Lesson]:
    lessons = schedule_db.get_lessons(day)
    return lessons
