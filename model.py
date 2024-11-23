from datetime import datetime

from aiogram.types import CallbackQuery

import datetime_utils as dt
import markups
from strings import Strings as s


async def send_select_day_message(callback: CallbackQuery):
    message_text = s.WEEKDAY
    weekdays_markup = markups.get_weekdays_markup()
    await callback.message.edit_text(text=message_text, reply_markup=weekdays_markup)
    await callback.answer()


async def send_set_manual_message(callback: CallbackQuery):
    message_text = s.SET_MANUAL
    await callback.message.edit_text(text=message_text)
    await callback.answer()


def get_day_schedule(day_callback: str, cday: datetime):
    weekday: int = int(day_callback[len(day_callback) - 1])
    day: datetime = dt.get_datetime_from_weekday(weekday)
    lessons = get_day_lessons(day)
    schedule = get_schedule(lessons)

def get_schedule(lessons: list[datetime]) -> list[datetime]:
    pass


def get_day_lessons(day: datetime) -> list[datetime]:
    # TODO get from dp lessons for day
    pass
