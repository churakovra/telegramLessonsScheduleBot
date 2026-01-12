from uuid import UUID

from aiogram.filters.callback_data import CallbackData

from app.utils.enums.bot_values import OperationType
from app.utils.keyboard.callback_factories.mixins import SpecifyWeekMixin


class SendSlots(CallbackData, prefix="send-slots-to-students"):
    teacher_uuid: UUID
    operation_type: OperationType


class ResendSlots(CallbackData, prefix="resend-s-t-s"):
    teacher_uuid: UUID
    student_chat_id: int


class DaysForStudents(CallbackData, prefix="days-for-students"):
    day: str
    teacher_uuid: UUID


class SlotsForStudents(CallbackData, prefix="fabslots"):
    uuid_slot: UUID


class UpdateSlots(SpecifyWeekMixin, prefix="update-slots"):
    pass


class ListSlots(SpecifyWeekMixin, prefix="list-slots"):
    pass
