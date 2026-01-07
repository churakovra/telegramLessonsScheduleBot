from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class BaseDelete(CallbackData, prefix="delete-b"):
    uuid: UUID
    confirmed: bool = False
