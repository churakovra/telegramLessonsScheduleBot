class BotStrings:
    class Common:
        GREETING = "Привет, {user}! Я буду сообщать тебе когда у твоего преподавателя появятся окошки для занятий"
        MENU = "Привет! Ты в главном меню. Жми кнопочки и управляй мечтой!"
        SUB_MENU = "Выбери необходимое действие:"
        SPECIFY_WEEK = "Отлично! Для начала выбери неделю:"
        NOT_ENOUGH_RIGHTS = "Ошибка. Недостаточно прав для выполнения данной операции"
        CONFIRM_OPERATION = "Подтвердите операцию:"

    class Errors:
        INVALID_INPUT = "Неверный ввод. Пожалуйста, отправьте текстовое сообщение."

    class Teacher:
        # * Bind user
        TEACHER_STUDENT_ADD = "Отправь логин ученика (можно несколько через пробел)"
        TEACHER_STUDENTS_ADD_SUCCESS = "Успешно добавил студентов {student}. Теперь они будут получать сообщения о новых окошках"
        TEACHER_STUDENT_ADD_SUCCESS = "Успешно добавил студента {student}. Теперь он будут получать сообщения о новых окошках"
        TEACHER_STUDENT_ADD_UNKNOWN_STUDENTS = "Смогу прикрепить всех кроме {student}\nПроверь, правильно ли указаны их логины"
        TEACHER_STUDENT_ADD_UNKNOWN_STUDENT = (
            "Смогу прикрепить всех кроме {student}\nПроверь, правильно ли указан логин"
        )

        # * Unbind user
        TEACHER_STUDENT_DELETE = "Выбери ученика для удаления: "
        TEACHER_STUDENT_DELETE_CONFIRMATION_REQUEST = (
            "Вы уверены, что хотите удалить ученика?"
        )
        TEACHER_STUDENT_DELETE_SUCCESS = "Ученик успешно удален!"

        TEACHER_STUDENTS_NOT_FOUND = (
            "Студенты не найдены\nПроверь, правильно ли указаны данные"
        )

        TEACHER_STUDENTS_LIST = "Ваши ученики:"

        STUDENT_ATTACH_LESSONS_LIST = "Выбери урок:"
        STUDENT_ATTACH_SUCCESS = "Ученик успешно записан на предмет"
        STUDENT_DETACH_SUCCESS = "Ученик успешно откреплён!"

        # * Lessons
        TEACHER_LESSON_ADD_LABEL = "Как называется предмет?"
        TEACHER_LESSON_ADD_DURATION = "Какая продолжительность в минутах?"
        TEACHER_LESSON_ADD_DURATION_ERROR = (
            "Неверный формат. Укажи пожалуйста в минутах:  45, 60, 90..."
        )
        TEACHER_LESSON_ADD_PRICE = "Стоимость?"
        TEACHER_LESSON_ADD_PRICE_ERROR = (
            "Неверный формат. Укажи пожалуйста сумму: 500, 800, 1500..."
        )
        TEACHER_LESSON_ADD_SUCCESS = "Предмет успешно добавлен"
        TEACHER_LESSON_DELETE = "Выбери предмет для удаления:"
        TEACHER_LESSONS_WERE_NOT_FOUND = "Ошибка. Предметы не найдены"
        TEACHER_LESSON_DELETE_CONFIRMATION_REQUEST = "Вы уверены, что хотите удалить урок? Это автоматически удалит и записи учеников."
        TEACHER_LESSON_DELETE_SUCCESS = "Предмет успешно удалён"
        TEACHER_LESSON_UPDATE = "Выбери предмет для изменения:"
        TEACHER_LESSON_UPDATE_SELECT_SPEC = "Что поменять?"
        TEACHER_LESSON_UPDATE_SUCCESS = "Предмет успешно обновлен"
        TEACHER_LESSON_LIST = "Список Ваших уроков:"

        # * Slots
        SLOTS_ADD = "Отправь окошки"
        SLOTS_LIST = "Ваши окошки:"
        SLOTS_PROCESSING_SUCCESS = (
            "Окошки добавлены🥳\nНажми кнопку, чтобы отправить их студентам"
        )
        SLOTS_FAILURE = "Отправь окошки еще раз"
        SLOTS_NOT_FOUND = "Окошки не найдены"
        NOT_ENOUGH_RIGHTS = "Ошибка. Вы должны быть в статусе Преподаватель для выполнения данного действия"
        SLOT_IS_TAKEN = "@{student} записался на урок {slot_time}"
        CALLBACK_SLOTS_CORRECT = "slots_correct"
        CALLBACK_SLOTS_INCORRECT = "slots_incorrect"
        SLOT_INFO = "Информация об окошке"
        SLOT_DELETE_SUCCESS = "Слот успешно удалён!"

    class Student:
        SLOTS_ADDED = "Привет! Выбери окошки на следующую неделю:"
        SLOTS_UPDATED = "Привет! Окошки обновились, выбери пожалуйста новое время:"
        SLOTS_ASSIGN_SUCCESS = (
            "Отлично! Вы записаны к @{teacher}, время занятия {slot_time}"
        )

    class Admin:
        MAKE_TEACHER_COMMAND_IS_EMPTY = (
            "Ошибка. Используйте команду в виде /make_teacher <username>"
        )
        MAKE_TEACHER_NOT_ENOUGH_RIGHTS = "Ошибка. Вы должны быть администратором бота для выполнения данного действия"
        MAKE_TEACHER_STATUS_ERROR = "Ошибка. Вы должны быть в статусе Администратор, а пользователь в статусе Ученик"
        MAKE_TEACHER_SUCCESS = (
            'Пользователю {user} успешно добавлен статус "Преподаватель"'
        )
        MAKE_TEACHER_FAILURE = (
            "Ошибка. Не получилось сделать пользователя преподавателем"
        )

    class User:
        USER_INFO = "Информация"
        USER_INFO_ERROR = "Ошибка. Пользователь не найден"
        USERNAME_REQUIRED = (
            "Для регистрации установите имя пользователя в настройках Telegram"
        )
        CALLBACK_USER_INFO = "user_info"

    class Menu:
        YES = "Да"
        NO = "Нет"
        MENU = "Меню"
        BACK = "Назад"
        CANCEL = "Отмена"
        SEND = "Отправить"
        UPDATE = "Изменить"
        ATTACH = "Прикрепить к уроку"
        DETACH = "Открепить от урока"
        DELETE = "Удалить"
        BIND_ANOTHER_SLOT = "Записаться ещё"
        CURRENT_WEEK = "Текущая"
        NEXT_WEEK = "Следующая"
