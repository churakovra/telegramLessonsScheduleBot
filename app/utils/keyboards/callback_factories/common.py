from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class BaseUpdate(CallbackData, prefix="delete-b"):
    uuid: UUID
    spec: str | None = None


class BaseDelete(CallbackData, prefix="delete-b"):
    uuid: UUID
    confirmed: bool = False
