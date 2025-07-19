from app.utils.enums.menu_type import MenuType
from app.utils.keyboards.callback_factories.base import BaseMenuCallback

teacher_menu = {
    "Ученики": MenuType.TEACHER_STUDENT,
    "Окошки": MenuType.TEACHER_SLOT,
    "Уроки": MenuType.TEACHER_LESSON,
}

student_menu = {
    "Учителя": MenuType.STUDENT_TEACHER,
    "Занятия": MenuType.STUDENT_SLOT,
    "Предметы": MenuType.STUDENT_LESSON,
}

admin_menu = {
    "Пока командами": MenuType.ADMIN_TEMP
}


class MainMenuCallback(BaseMenuCallback, prefix="fab-main-menu"):
    pass
