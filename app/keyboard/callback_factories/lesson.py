from app.keyboard.callback_factories.common import (
    BaseCallback,
    BaseDelete,
    BaseList,
    BaseUpdate,
)


class LessonCallback(BaseCallback, prefix="lesson"):
    pass


class LessonList(BaseList, prefix="list-l"):
    pass


class LessonDelete(BaseDelete, prefix="delete-l"):
    pass


class LessonUpdate(BaseUpdate, prefix="update-l"):
    pass
