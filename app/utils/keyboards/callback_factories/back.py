from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class BackCallback(CallbackData, prefix="back-button"):
    parent_keyboard: str
    teacher_uuid: UUID | None = None
