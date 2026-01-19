from app.keyboard.callback_factories.common import (
    BaseCreateCallback,
    BaseDeleteCallback,
    BaseInfoCallback,
    BaseListCallback,
    BaseOperationCallback,
    BaseUpdateCallback,
)
from app.utils.enums.bot_values import ActionType


class StudentCreateCallback(BaseCreateCallback, prefix="create-s"):
    pass


class StudentInfoCallback(BaseInfoCallback, prefix="info-s"):
    pass


class StudentListCallback(BaseListCallback, prefix="list-s"):
    pass


class StudentDeleteCallback(BaseDeleteCallback, prefix="delete-s"):
    pass


class StudentUpdateCallback(BaseUpdateCallback, prefix="update-s"):
    pass


class StudentAttachCallback(BaseOperationCallback, prefix="attach-s"):
    pass


class StudentDetachCallback(BaseOperationCallback, prefix="detach-s"):
    pass
