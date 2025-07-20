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

    SLOTS_PROCESSING_SUCCESS_ANSWER: str = "Отлично! Отправил окошки ученикам 🤝"
    SLOTS_FAILURE_ANSWER: str = "Отправьте окошки еще раз"
    SLOTS_NOT_ENOUGH_RIGHTS = "Ошибка. Вы должны быть в статусе Преподаватель для выполнения данного действия"
    SLOTS_ASSIGN_SUCCESS_ANSWER: str = "Отлично! Вы записаны к @{}, время занятия {}"

    MAKE_TEACHER_COMMAND_IS_EMPTY = "Ошибка. Используйте команду в виде /make_teacher <username>"
    MAKE_TEACHER_NOT_ENOUGH_RIGHTS = "Ошибка. Вы должны быть администратором бота для выполнения данного действия"
    MAKE_TEACHER_STATUS_ERROR = "Ошибка. Вы должны быть в статусе Администратор, а пользователь в статусе Ученик"
    MAKE_TEACHER_SUCCESS = 'Пользователю {} успешно добавлен статус "Преподаватель"'
    MAKE_TEACHER_FAILURE = "Ошибка. Не получилось сделать пользователя преподавателем"

    TEACHER_ADD_STUDENT = ("Отправь логин ученика без @, например `kdianitta`\n"
                           "Либо, если хочешь добавить несколько учеников, отправь их через пробел: `kdianitta1 kdianitta2...`")
    TEACHER_ADD_STUDENT_UNKNOWN_STUDENTS = ("Смогу прикрепить всех кроме {}. Их не смог найти :(\n"
                                            f"Проверь, правильно ли указаны их логины")
    TEACHER_ADD_STUDENT_SUCCESS = "Успешно добавил студента(-ов) {}. Теперь они будут получать сообщения о новых окошках"
    TEACHER_ADD_LESSON_LABEL = "Как называется предмет?"
    TEACHER_ADD_LESSON_DURATION = "Какая продолжительность в минутах? 45, 60, 90...?"
    TEACHER_ADD_LESSON_PRICE = "Стоимость?"
    TEACHER_ADD_LESSON_SUCCESS = "Предмет {} успешно добавлен"


bot_strings = BotStrings()
