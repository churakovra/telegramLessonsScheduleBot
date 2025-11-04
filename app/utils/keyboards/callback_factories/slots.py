from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class SendSlots(CallbackData, prefix="send-slots-to-students"):
    teacher_uuid: UUID


class ResendSlots(CallbackData, prefix="resend-s-t-s"):
    teacher_uuid: UUID
    student_chat_id: int

class DaysForStudents(CallbackData, prefix="days-for-students"):
    day: str
    teacher_uuid: UUID


class SlotsForStudents(CallbackData, prefix="fabslots"):
    uuid_slot: UUID
