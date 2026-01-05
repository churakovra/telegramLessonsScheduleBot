
from uuid import UUID
from aiogram.filters.callback_data import CallbackData

class LessonDelete(CallbackData, prefix="delete-l"):
    lesson_uuid: UUID