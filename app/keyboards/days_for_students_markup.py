from uuid import UUID

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class DaysForStudents(CallbackData, prefix="fabday"):
    day_uuid: UUID


def get_days_for_students_markup(slots: dict[str, UUID]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for day, day_uuid in slots:
        builder.button(
            text=day,
            callback_data=DaysForStudents(day_uuid=day_uuid)
        )
    builder.adjust(1)
    return builder.as_markup()
