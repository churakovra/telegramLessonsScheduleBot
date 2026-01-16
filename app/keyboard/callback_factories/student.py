from app.keyboard.callback_factories.common import BaseCallback, BaseDelete, BaseList, BaseUpdate


class StudentCallback(BaseCallback, prefix="student"):
    pass


class StudentList(BaseList, prefix="list-s"):
    pass


class StudentDelete(BaseDelete, prefix="delete-s"):
    pass


class StudentUpdate(BaseUpdate, prefix="update-s"):
    pass
