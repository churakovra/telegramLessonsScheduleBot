from app.keyboard.callback_factories.common import BaseDelete, BaseList, BaseUpdate


class LessonList(BaseList, prefix="list-l"):
    pass


class LessonDelete(BaseDelete, prefix="delete-l"):
    pass


class LessonUpdate(BaseUpdate, prefix="update-l"):
    pass