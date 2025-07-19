from uuid import UUID

from aiogram.filters.callback_data import CallbackData

from app.schemas.slot_dto import SlotDTO


class DaysForStudents(CallbackData, prefix="fabday"):
    day_num: int
    slots: list[SlotDTO]
    teacher_uuid: UUID
