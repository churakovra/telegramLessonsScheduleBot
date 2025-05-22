from uuid import UUID

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.repositories.slots_repo import SlotsRepo
from app.utils.datetime_utils import time_format_HM


class SlotsForStudents(CallbackData, prefix="fabslots"):
    uuid_slot: UUID


async def get_slots_for_students_markup(uuid_day: UUID) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    slots = await SlotsRepo.get_slots(uuid_day)
    for slot in slots:
        time_str = slot.dt_start.strftime(time_format_HM)
        builder.button(
            text=time_str,
            callback_data=SlotsForStudents(uuid_slot=slot.uuid_slot)
        )
    # builder.button(
    #     text="Назад",
    #     callback_data="назад"
    # )
    builder.adjust(1)
    return builder.as_markup()
