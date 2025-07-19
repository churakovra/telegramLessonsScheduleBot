from uuid import UUID

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.schemas.slot_dto import SlotDTO
from app.utils.datetime_utils import time_format_HM
from app.utils.keyboards.callback_factories.back import BackCallback
from app.utils.keyboards.callback_factories.slots_for_students import SlotsForStudents


def get_slots_for_students_markup(slots: list[SlotDTO], teacher_uuid: UUID) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for slot in slots:
        time_str = slot.dt_start.strftime(time_format_HM)
        builder.button(
            text=time_str,
            callback_data=SlotsForStudents(uuid_slot=slot.uuid_slot)
        )
    builder.button(
        text="Назад",
        callback_data=BackCallback(
            current_level="slots_for_students",
            parent_keyboard="days_for_students",
            teacher_uuid=teacher_uuid
        )
    )
    builder.adjust(1)
    return builder.as_markup()
