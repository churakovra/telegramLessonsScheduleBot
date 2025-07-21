from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class DaysForStudentsCallback(CallbackData, prefix="days-for-students"):
    day: str
    teacher_uuid: UUID
