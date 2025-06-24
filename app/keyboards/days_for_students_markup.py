import calendar

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.schemas.slot_dto import SlotDTO
from app.utils.datetime_utils import WEEKDAYS


class DaysForStudents(CallbackData, prefix="fabday"):
    day_num: int
    slots: list[SlotDTO]


def get_days_for_students_markup(slots: list[SlotDTO]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    day_num = slots[0].dt_start.day
    day_slots = list()
    for slot in slots:
        if slot.dt_start.day == day_num:
            day_slots.append(slot.uuid)
        else:
            weekday_num = calendar.weekday(
                slot.dt_start.year,
                slot.dt_start.month,
                slot.dt_start.day
            )  # Получаем номер дня недели в зависимости от даты
            weekday = WEEKDAYS[weekday_num][2]
            builder.button(
                text=weekday,
                callback_data=DaysForStudents(day_num=day_num, slots=day_slots)
            )

            day_num = slot.dt_start.day
            day_slots.clear()

    builder.adjust(1)
    return builder.as_markup()
