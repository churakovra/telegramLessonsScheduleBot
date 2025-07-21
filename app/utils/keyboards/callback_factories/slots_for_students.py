from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class SlotsForStudents(CallbackData, prefix="fabslots"):
    uuid_slot: UUID