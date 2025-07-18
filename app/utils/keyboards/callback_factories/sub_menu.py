from app.utils.keyboards.callback_factories.base import BaseMenuCallback
from app.utils.bot_strings import bot_strings as bt

teacher_student = {
    "Добавить ученика": bt.CALLBACK_GROUP_TEACHER_STUDENT_ADD,
    "Изменить ученика": bt.CALLBACK_GROUP_TEACHER_STUDENT_EDIT,
    "Мои ученики": bt.CALLBACK_GROUP_TEACHER_STUDENT_LIST,
    "Удалить ученика": bt.CALLBACK_GROUP_TEACHER_STUDENT_DELETE,
}

teacher_slot = {
    "Добавить окошки": bt.CALLBACK_GROUP_TEACHER_SLOT_ADD,
    "Изменить окошки": bt.CALLBACK_GROUP_TEACHER_SLOT_EDIT,
    "Записать ученика в окошко": bt.CALLBACK_GROUP_TEACHER_SLOT_SPOT,
    "Мои окошки": bt.CALLBACK_GROUP_TEACHER_SLOT_LIST,
    "Удалить окошко": bt.CALLBACK_GROUP_TEACHER_SLOT_DELETE,
}

teacher_lesson = {
    "Добавить предмет": bt.CALLBACK_GROUP_TEACHER_LESSON_ADD,
    "Изменить предмет": bt.CALLBACK_GROUP_TEACHER_LESSON_EDIT,
    "Мои предметы": bt.CALLBACK_GROUP_TEACHER_LESSON_LIST,
    "Удалить предмет": bt.CALLBACK_GROUP_TEACHER_LESSON_DELETE,
}

student_teacher = {
    "Мои учителя": bt.CALLBACK_GROUP_TEACHER_LESSON_LIST,
}

student_slot = {
    "Мои занятия": bt.CALLBACK_GROUP_TEACHER_LESSON_LIST,
}

student_lesson = {
    "Мои предметы": bt.CALLBACK_GROUP_TEACHER_LESSON_LIST,
}


class SubMenuCallback(BaseMenuCallback, prefix="sub-menu-callback"):
    pass