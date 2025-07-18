from dataclasses import dataclass


@dataclass
class BotStrings(str):
    GREETING: str = (
        "Привет, {}! Я буду сообщать тебе когда у твоего преподавателя появятся окошки для занятий"
    )
    MENU: str = (
        "Привет, {}! Ты в главном меню. Жми кнопочки с умом и помни: С большой силой приходит большая ответственность!"
    )

    YES: str = "Да"
    NO: str = "Нет"

    USER_INFO: str = "Информация"
    USER_INFO_ERROR: str = "Ошибка. Пользователь не найден."
    CALLBACK_USER_INFO: str = "user_info"

    CALLBACK_SLOTS_CORRECT: str = "slots_correct"
    CALLBACK_SLOTS_INCORRECT: str = "slots_incorrect"

    CALLBACK_GROUP_TEACHER = "cg-t"
    CALLBACK_GROUP_TEACHER_STUDENT = "cg-t-student"
    CALLBACK_GROUP_TEACHER_STUDENT_ADD = "cg-t-student_add"
    CALLBACK_GROUP_TEACHER_STUDENT_EDIT = "cg-t-student_edit"
    CALLBACK_GROUP_TEACHER_STUDENT_LIST = "cg-t-student_list"
    CALLBACK_GROUP_TEACHER_STUDENT_DELETE = "cg-t-student_delete"
    CALLBACK_GROUP_TEACHER_SLOT = "cg-t-slot"
    CALLBACK_GROUP_TEACHER_SLOT_ADD = "cg-t-slot_add"
    CALLBACK_GROUP_TEACHER_SLOT_EDIT = "cg-t-slot_edit"
    CALLBACK_GROUP_TEACHER_SLOT_SPOT = "cg-t-slot_spot"
    CALLBACK_GROUP_TEACHER_SLOT_LIST = "cg-t-slot_list"
    CALLBACK_GROUP_TEACHER_SLOT_DELETE = "cg-t-slot_delete"
    CALLBACK_GROUP_TEACHER_LESSON = "cg-t-lesson"
    CALLBACK_GROUP_TEACHER_LESSON_ADD = "cg-t-lesson_add"
    CALLBACK_GROUP_TEACHER_LESSON_EDIT = "cg-t-lesson_edit"
    CALLBACK_GROUP_TEACHER_LESSON_LIST = "cg-t-lesson_list"
    CALLBACK_GROUP_TEACHER_LESSON_DELETE = "cg-t-lesson_delete"

    CALLBACK_GROUP_STUDENT = "cg-s"
    CALLBACK_GROUP_STUDENT_TEACHER = "cg-s-teacher"
    CALLBACK_GROUP_STUDENT_TEACHER_LIST = "cg-s-teacher_list"
    CALLBACK_GROUP_STUDENT_SLOT = "cg-s-slot"
    CALLBACK_GROUP_STUDENT_SLOT_LIST = "cg-s-slot_list"
    CALLBACK_GROUP_STUDENT_LESSON = "cg-s-lesson"
    CALLBACK_GROUP_STUDENT_LESSON_LIST = "cg-s-lesson_list"

    SLOTS_PROCESSING_SUCCESS_ANSWER: str = "Отлично! Отправил окошки ученикам 🤝"
    SLOTS_FAILURE_ANSWER: str = "Отправьте окошки еще раз"
    SLOTS_NOT_ENOUGH_RIGHTS = "Ошибка. Вы должны быть в статусе Преподаватель для выполнения данного действия"
    SLOTS_ASSIGN_SUCCESS_ANSWER: str = "Отлично! Вы записаны к @{}, время занятия {}"

    MAKE_TEACHER_COMMAND_IS_EMPTY = "Ошибка. Используйте команду в виде /make_teacher <username>"
    MAKE_TEACHER_NOT_ENOUGH_RIGHTS = "Ошибка. Вы должны быть администратором бота для выполнения данного действия"
    MAKE_TEACHER_STATUS_ERROR = "Ошибка. Вы должны быть в статусе Администратор, а пользователь в статусе Ученик"
    MAKE_TEACHER_SUCCESS = 'Пользователю {} успешно добавлен статус "Преподаватель"'
    MAKE_TEACHER_FAILURE = "Ошибка. Не получилось сделать пользователя преподавателем"


bot_strings = BotStrings()
