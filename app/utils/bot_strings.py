from dataclasses import dataclass


@dataclass
class BotStrings:
    GREETING: str = ("Привет, {}! Я буду сообщать тебе когда у твоего преподавателя появятся окошки для занятий. "
                     "Помоги мне тебя прикрепить, напиши логин преподавателя (например твой логин - {}).")
    WEEKDAY: str = "Выбери день недели:"
    APPROVE_ASK: str = "Подтверди запись 🤗"
    APPROVE_ANSW: str = "Подтверждаю 🙂‍↕️"

    YES: str = "Да"
    NO: str = "Нет"

    USER_INFO: str = "Информация"
    USER_INFO_ERROR: str = "Ошибка. Пользователь не найден."
    CALLBACK_USER_INFO: str = "user_info"

    CALLBACK_SLOTS_CORRECT: str = "slots_correct"
    CALLBACK_SLOTS_INCORRECT: str = "slots_incorrect"

    SLOTS_PROCESSING_SUCCESS_ANSWER: str = "Отлично! Отправил окошки ученикам 🤝"
    SLOTS_FAILURE_ANSWER: str = "Отправьте окошки еще раз"
    SLOTS_NOT_ENOUGH_RIGHTS = "Ошибка. Вы должны быть в статусе Преподаватель для выполнения данного действия"
    SLOTS_ASSIGN_SUCCESS_ANSWER: str = "Отлично! Вы записаны к @{}, время занятия {}"

    MAKE_TEACHER_COMMAND_IS_EMPTY = "Ошибка. Используйте команду в виде /make_teacher <username>"
    MAKE_TEACHER_NOT_ENOUGH_RIGHTS = "Ошибка. Вы должны быть администратором бота для выполнения данного действия"
    MAKE_TEACHER_STATUS_ERROR = "Ошибка. Вы должны быть в статусе Администратор, а пользователь в статусе Ученик"
    MAKE_TEACHER_SUCCESS = "Пользователь успешно переведен из статуса Ученик в статус Преподаватель"
    MAKE_TEACHER_FAILURE = "Ошибка. Не получилось сделать пользователя преподавателем"


bot_strings = BotStrings()
