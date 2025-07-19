from app.utils.bot_strings import bot_strings as bt
from app.utils.keyboards.callback_factories.base import BaseMenuCallback

teacher_menu = {
    "Ученики": bt.CALLBACK_GROUP_TEACHER_STUDENT,
    "Окошки": bt.CALLBACK_GROUP_TEACHER_SLOT,
    "Уроки": bt.CALLBACK_GROUP_TEACHER_LESSON,
}

student_menu = {
    "Учителя": bt.CALLBACK_GROUP_STUDENT_TEACHER,
    "Занятия": bt.CALLBACK_GROUP_STUDENT_SLOT,
    "Предметы": bt.CALLBACK_GROUP_STUDENT_LESSON,
}


class MainMenuCallback(BaseMenuCallback, prefix="fab-main-menu"):
    pass
