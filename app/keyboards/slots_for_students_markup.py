from uuid import UUID

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.models.lesson_dto import LessonDTO
from app.utils.datetime_utils import time_format_HM


class SlotsForStudents(CallbackData, prefix="fabslots"):
    uuid_slot: UUID


class BackPressed(CallbackData, prefix="back"):
    chat_id: int


def get_slots_for_students_markup(slots: list[LessonDTO], chat_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for slot in slots:
        time_str = slot.dt_start.strftime(time_format_HM)
        builder.button(
            text=time_str,
            callback_data=SlotsForStudents(uuid_slot=slot.uuid_slot)
        )
    builder.button(
        text="Назад",
        callback_data=BackPressed(chat_id=chat_id)
    )
    builder.adjust(1)
    return builder.as_markup()
