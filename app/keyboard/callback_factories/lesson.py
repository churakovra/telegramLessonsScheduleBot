from app.keyboard.callback_factories.common import (
    BaseCallback,
    BaseDeleteCallback,
    BaseInfoCallback,
    BaseListCallback,
    BaseUpdateCallback,
)


class LessonCallback(BaseCallback, prefix="lesson"):
    pass


class LessonInfoCallback(BaseInfoCallback, prefix="info-l"):
    pass


class LessonListCallback(BaseListCallback, prefix="list-l"):
    pass


class LessonDeleteCallback(BaseDeleteCallback, prefix="delete-l"):
    pass


class LessonUpdateCallback(BaseUpdateCallback, prefix="update-l"):
    pass
