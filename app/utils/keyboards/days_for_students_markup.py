import calendar
from uuid import UUID

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.schemas.slot_dto import SlotDTO
from app.utils.datetime_utils import WEEKDAYS, day_format
from app.utils.keyboards.callback_factories.days_for_students import DaysForStudentsCallback


def get_days_for_students_markup(slots: list[SlotDTO], teacher_uuid: UUID) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    prev_slot_date = None
    for slot in slots:
        slot_date = slot.dt_start.date()
        if slot_date != prev_slot_date:
            day_number = calendar.weekday(slot_date.year, slot_date.month, slot_date.day)
            day_name = WEEKDAYS[day_number][2]
            builder.button(
                text=day_name,
                callback_data=DaysForStudentsCallback(day=slot_date.strftime(day_format), teacher_uuid=teacher_uuid)
            )
            prev_slot_date = slot_date

    builder.adjust(1)
    return builder.as_markup()
