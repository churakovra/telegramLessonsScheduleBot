from app.keyboard.callback_factories.common import (
    BaseCreateCallback,
    BaseDeleteCallback,
    BaseListCallback,
)


class NotificationCreateCallback(BaseCreateCallback, prefix="create-n"):
    pass


class NotificationListCallback(BaseListCallback, prefix="list-n"):
    pass


class NotificationDeleteCallback(BaseDeleteCallback, prefix="delete-n"):
    pass
