from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class SendSlotsCallback(CallbackData, prefix="send-slots-to-students"):
    teacher_uuid: UUID


class DaysForStudentsCallback(CallbackData, prefix="days-for-students"):
    day: str
    teacher_uuid: UUID


class SlotsForStudents(CallbackData, prefix="fabslots"):
    uuid_slot: UUID
