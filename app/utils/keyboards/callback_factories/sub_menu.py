from app.utils.enums.menu_type import MenuType
from app.utils.keyboards.callback_factories.base import BaseMenuCallback

teacher_student = {
    "Добавить ученика": MenuType.TEACHER_STUDENT_ADD,
    "Изменить ученика": MenuType.TEACHER_STUDENT_EDIT,
    "Мои ученики": MenuType.TEACHER_STUDENT_LIST,
    "Удалить ученика": MenuType.TEACHER_STUDENT_DELETE,
}

teacher_slot = {
    "Добавить окошки": MenuType.TEACHER_SLOT_ADD,
    "Изменить окошки": MenuType.TEACHER_SLOT_EDIT,
    "Записать ученика в окошко": MenuType.TEACHER_SLOT_SPOT,
    "Мои окошки": MenuType.TEACHER_SLOT_LIST,
    "Удалить окошко": MenuType.TEACHER_SLOT_DELETE,
}

teacher_lesson = {
    "Добавить предмет": MenuType.TEACHER_LESSON_ADD,
    "Изменить предмет": MenuType.TEACHER_LESSON_EDIT,
    "Мои предметы": MenuType.TEACHER_LESSON_LIST,
    "Удалить предмет": MenuType.TEACHER_LESSON_DELETE,
}

student_teacher = {
    "Мои учителя": MenuType.STUDENT_TEACHER_LIST,
}

student_slot = {
    "Мои занятия": MenuType.STUDENT_SLOT_LIST,
}

student_lesson = {
    "Мои предметы": MenuType.STUDENT_LESSON_LIST,
}

admin_temp = {
    "Пока командой": MenuType.ADMIN_TEMP
}


class SubMenuCallback(BaseMenuCallback, prefix="sub-menu-callback"):
    pass
