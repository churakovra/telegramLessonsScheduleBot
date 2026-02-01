from uuid import UUID

from aiogram.filters.callback_data import CallbackData

from app.utils.enums.bot_values import ActionType


class BaseCallback(CallbackData, prefix="b"):
    action: ActionType


class BaseOperationCallback(CallbackData, prefix="b-o"):
    pass


class BaseCreateCallback(BaseOperationCallback, prefix="create-b"):
    pass


class BaseInfoCallback(BaseOperationCallback, prefix="info-b"):
    uuid: UUID


class BaseListCallback(BaseOperationCallback, prefix="list-b"):
    pass


class BaseUpdateCallback(BaseOperationCallback, prefix="update-b"):
    uuid: UUID
    spec: str | None = None


class BaseDeleteCallback(BaseOperationCallback, prefix="delete-b"):
    uuid: UUID
    confirmed: bool = False


class BaseAssignCallback(BaseOperationCallback, prefix="assign-s"):
    uuid: UUID
    id_lesson: int | None = None