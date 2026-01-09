from uuid import UUID

from aiogram.filters.callback_data import CallbackData

class BaseCallback(CallbackData, prefix="b"):
    uuid: UUID


class BaseList(BaseCallback, prefix="list-b"):
    uuid:UUID

class BaseUpdate(BaseCallback, prefix="update-b"):
    uuid: UUID
    spec: str | None = None


class BaseDelete(BaseCallback, prefix="delete-b"):
    uuid: UUID
    confirmed: bool = False
