from uuid import UUID

from aiogram.filters.callback_data import CallbackData

from app.keyboard.callback_factories.common import (
    BaseCreateCallback,
    BaseDeleteCallback,
    BaseInfoCallback,
    BaseListCallback,
    BaseUpdateCallback,
)
from app.keyboard.callback_factories.mixins import SpecifyWeekMixin


class SlotCreateCallback(BaseCreateCallback, SpecifyWeekMixin, prefix="create-sl"):
    pass


class SlotInfoCallback(BaseInfoCallback, prefix="info-sl"):
    pass


class SlotListCallback(BaseListCallback, SpecifyWeekMixin, prefix="list-sl"):
    pass


class SlotsUpdateCallback(SlotCreateCallback, SpecifyWeekMixin, prefix="update-slts"):
    pass


class SlotUpdateCallback(BaseUpdateCallback, prefix="update-sl"):
    pass


class SlotDeleteCallback(BaseDeleteCallback, prefix="delete-sl"):
    pass


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
