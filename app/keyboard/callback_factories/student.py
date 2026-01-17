from app.keyboard.callback_factories.common import BaseCallback, BaseDeleteCallback, BaseInfoCallback, BaseListCallback, BaseUpdateCallback


class StudentCallback(BaseCallback, prefix="student"):
    pass


class StudentInfoCallback(BaseInfoCallback, prefix="info-s"):
    pass


class StudentListCallback(BaseListCallback, prefix="list-s"):
    pass


class StudentDeleteCallback(BaseDeleteCallback, prefix="delete-s"):
    pass


class StudentUpdateCallback(BaseUpdateCallback, prefix="update-s"):
    pass
