from app.utils.keyboards.callback_factories.common import BaseDelete, BaseUpdate


class LessonDelete(BaseDelete, prefix="delete-l"):
    pass


class LessonUpdate(BaseUpdate, prefix="update-l"):
    pass