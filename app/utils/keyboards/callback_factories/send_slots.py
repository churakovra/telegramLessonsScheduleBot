from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class SendSlotsCallback(CallbackData, prefix="send-slots-to-students"):
    teacher_uuid: UUID
