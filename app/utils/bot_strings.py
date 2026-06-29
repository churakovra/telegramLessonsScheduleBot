class BotStrings:
    class Common:
        WEEKDAY_LABELS = [
            "Понедельник",
            "Вторник",
            "Среда",
            "Четверг",
            "Пятница",
            "Суббота",
            "Воскресенье",
        ]
        WEEKDAY_SHORT_LABELS = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        GREETING = "Привет, {user}! Я буду сообщать тебе когда у твоего преподавателя появятся окошки для занятий"
        START_WELCOME = "👋 Добро пожаловать в Slotty, {name}!"
        START_NEW_STUDENT = (
            "Вы зарегистрированы как ученик. Вот что вы можете:\n"
            "• Найти преподавателя в разделе Преподаватели\n"
            "• Отправить заявку на обучение\n"
            "• Получать расписание от преподавателя\n"
            "• Отслеживать свою статистику\n\n"
            "Используйте /menu для навигации или /help для справки."
        )
        START_RETURNING = "С возвращением! Используйте /menu чтобы открыть меню."
        MENU = "Привет! Ты в главном меню. Жми кнопочки и управляй мечтой!"
        SUB_MENU = "Выбери необходимое действие:"
        SPECIFY_WEEK = "Отлично! Для начала выбери неделю:"
        NOT_ENOUGH_RIGHTS = "Ошибка. Недостаточно прав для выполнения данной операции"
        CONFIRM_OPERATION = "Подтвердите операцию:"
        HELP = (
            "Slotty связывает преподавателей и учеников: преподаватель создаёт предметы "
            "и окошки, ученик записывается на доступное время.\n\n"
            "Команды:\n"
            "/start - начать работу с ботом\n"
            "/menu - открыть главное меню\n"
            "/cancel - отменить текущее действие\n"
            "/help - помощь и инструкции\n\n"
            "Ученикам:\n"
            "• Откройте /menu и раздел Преподаватели\n"
            "• Выберите преподавателя и отправьте заявку\n"
            "• После одобрения записывайтесь на окошки и проверяйте расписание\n\n"
            "Преподавателям:\n"
            "• Заполните Мой профиль, чтобы ученики понимали, чему вы учите\n"
            "• Добавляйте учеников вручную или принимайте заявки\n"
            "• Создавайте предметы, окошки и уведомления\n"
            "• Следите за переносами, отзывами и статистикой\n\n"
            "FAQ:\n"
            "Меня не добавили к преподавателю - что делать?\n"
            "Проверьте, что заявка отправлена в разделе Преподаватели, или напишите преподавателю напрямую."
        )

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
        SLOTS_CONFLICT = (
            "Некоторые слоты конфликтуют с существующими:\n"
            "{slots}\n\n"
            "Исправьте и попробуйте снова."
        )
        SLOTS_NOT_FOUND = "Окошки не найдены"
        NOT_ENOUGH_RIGHTS = "Ошибка. Вы должны быть в статусе Преподаватель для выполнения данного действия"
        SLOT_IS_TAKEN = "@{student} записался на урок {slot_time}"
        CALLBACK_SLOTS_CORRECT = "slots_correct"
        CALLBACK_SLOTS_INCORRECT = "slots_incorrect"
        SLOT_INFO = "Информация об окошке"
        SLOT_DELETE_SUCCESS = "Слот успешно удалён!"
        SLOT_CANCELLED_BY_STUDENT = "Ученик @{student} отменил запись на {slot_time}"

        # * Notifications
        NOTIFICATION_ADD_TEXT = "Отправь текст уведомления"
        NOTIFICATION_ADD_MINUTES = "За сколько минут до занятия отправлять?"
        NOTIFICATION_ADD_MINUTES_ERROR = "Неверный формат. Укажи число минут: 60, 120, 1440..."
        NOTIFICATION_ADD_SUCCESS = "Уведомление создано"
        NOTIFICATIONS_LIST = "Ваши уведомления:"
        NOTIFICATIONS_NOT_FOUND = "Уведомления не найдены"
        NOTIFICATION_DELETE_SUCCESS = "Уведомление удалено"

        # * Recurrence
        RECURRENCE_RULES = "Повторяющиеся окошки:"
        RECURRENCE_RULES_NOT_FOUND = "Повторяющиеся окошки не найдены"
        RECURRENCE_SELECT_DAY = "Выбери день недели"
        RECURRENCE_START_TIME = "Отправь время начала в формате HH:MM"
        RECURRENCE_END_TIME = "Отправь время окончания в формате HH:MM"
        RECURRENCE_DURATION = "Отправь длительность окошка в минутах"
        RECURRENCE_START_DATE = "Отправь дату начала в формате ДД.ММ.ГГГГ"
        RECURRENCE_END_DATE = "Отправь дату окончания в формате ДД.ММ.ГГГГ"
        RECURRENCE_CONFIRM = "Проверь правило:\n{summary}"
        RECURRENCE_SUMMARY = "День: {day}\nВремя: {time_start}-{time_end}\nДлительность: {duration} мин\nПериод: {date_start}-{date_end}"
        RECURRENCE_CREATE_SUCCESS = "Повторяющееся расписание создано"
        RECURRENCE_DELETE_SUCCESS = "Правило удалено"

        # * Reschedule
        RESCHEDULE_REQUESTS = "Запросы на перенос:"
        RESCHEDULE_REQUESTS_NOT_FOUND = "Запросов на перенос нет"
        RESCHEDULE_APPROVED = "Перенос одобрен: {new_time}"
        RESCHEDULE_REJECTED = "Перенос отклонён"
        RESCHEDULE_CREATED = "Ученик @{student} просит перенести занятие с {old_time} на {new_time}"

        # * Statistics
        STATISTICS_PERIOD = "Выбери период:"
        STATISTICS_NOT_FOUND = "Статистика пока пустая"
        FEEDBACK_NOT_FOUND = "Отзывов пока нет"
        FEEDBACK_LIST = "Отзывы:\nСредняя оценка: {average}"

        # * Join requests
        JOIN_REQUESTS = "Заявки от учеников:"
        JOIN_REQUESTS_NOT_FOUND = "Нет новых заявок"
        JOIN_REQUEST_APPROVED = "Заявка одобрена"
        JOIN_REQUEST_REJECTED = "Заявка отклонена"
        JOIN_REQUEST_CREATED = "Новая заявка от ученика @{student}"

        # * Profile
        PROFILE = (
            "Мой профиль\n\n"
            "Имя: {display_name}\n"
            "Предметы: {subjects}\n"
            "Описание: {bio}"
        )
        PROFILE_DISPLAY_NAME = "Отправьте имя для профиля или '-' чтобы пропустить"
        PROFILE_BIO = "Отправьте описание или '-' чтобы пропустить"
        PROFILE_SUBJECTS = "Отправьте предметы через запятую или '-' чтобы пропустить"
        PROFILE_SAVED = "Профиль сохранён"

    class Student:
        SLOTS_ADDED = "Привет! Выбери окошки на следующую неделю:"
        SLOTS_UPDATED = "Привет! Окошки обновились, выбери пожалуйста новое время:"
        SLOTS_ASSIGN_SUCCESS = (
            "Отлично! Вы записаны к @{teacher}, время занятия {slot_time}"
        )
        SCHEDULE = "Ваши занятия:"
        SCHEDULE_EMPTY = "У вас пока нет записей"
        WEEKLY_SCHEDULE_TITLE = "📅 Ваше расписание на неделю:"
        WEEKLY_SCHEDULE_EMPTY = "На ближайшую неделю занятий нет."
        WEEKLY_SCHEDULE_DAY = "{weekday} {date}:"
        WEEKLY_SCHEDULE_ITEM = "  • {time} — {lesson} с {teacher}"
        WEEKLY_SCHEDULE_TOTAL = "Всего: {count} занятия, {hours} часов"
        SLOT_CANCEL_SUCCESS = "Запись отменена"
        SLOT_CANCEL_CONFIRM = "Отменить запись на {slot_time}?"
        RESCHEDULE_DATE = "Отправь новую дату в формате ДД.ММ.ГГГГ"
        RESCHEDULE_TIME = "Отправь новое время в формате HH:MM"
        RESCHEDULE_CONFIRM = "Запросить перенос на {new_time}?"
        RESCHEDULE_SENT = "Запрос на перенос отправлен преподавателю"
        RESCHEDULE_APPROVED = "Перенос одобрен: {new_time}"
        RESCHEDULE_REJECTED = "Перенос отклонён"
        FEEDBACK_PROMPT = "Как прошло занятие? Оцените от 1 до 5:"
        FEEDBACK_COMMENT_QUESTION = "Спасибо! Хотите оставить комментарий?"
        FEEDBACK_COMMENT = "Отправьте комментарий"
        FEEDBACK_THANKS = "Спасибо за отзыв!"
        STATISTICS_PERIOD = "Выбери период:"
        STATISTICS_NOT_FOUND = "Статистика пока пустая"
        TEACHERS = "Преподаватели:"
        TEACHERS_NOT_FOUND = "Преподаватели пока не найдены"
        TEACHER_PROFILE = (
            "{name}\n\n"
            "Предметы: {subjects}\n"
            "Количество предметов: {subjects_count}\n"
            "Описание: {bio}"
        )
        JOIN_REQUEST_SENT = "Заявка отправлена преподавателю"
        JOIN_REQUEST_ALREADY_EXISTS = "Заявка уже отправлена или обработана"
        JOIN_REQUEST_APPROVED = "Заявка одобрена! Теперь вы ученик {teacher_name}"
        JOIN_REQUEST_REJECTED = "Заявка отклонена"

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
        DASHBOARD = (
            "📊 Админ-панель\n\n"
            "👥 Пользователей: {total_users}\n"
            "👨‍🏫 Преподавателей: {total_teachers}\n"
            "👨‍🎓 Учеников: {total_students}\n"
            "📅 Уроков за неделю: {total_lessons_this_week}\n"
            "🔥 Активных преподавателей: {active_teachers_this_week}"
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
        NOTIFICATIONS = "Уведомления"
        CREATE_NOTIFICATION = "Создать уведомление"
        MY_NOTIFICATIONS = "Мои уведомления"
        STATISTICS = "Статистика"
        ADMIN_DASHBOARD = "Админ-панель"
        REFRESH = "Обновить"
        WEEKLY_SCHEDULE = "📅 На неделю"
        CANCEL_SLOT = "Отменить запись"
        RESCHEDULE_SLOT = "Перенести"
        RECURRENCE = "Повторяющиеся окошки"
        CREATE_RECURRENCE = "Создать правило"
        RESCHEDULE_REQUESTS = "Запросы на перенос"
        APPROVE = "Одобрить"
        REJECT = "Отклонить"
        FEEDBACK = "Отзывы"
        WEEK = "Неделя"
        MONTH = "Месяц"
        YEAR = "Год"
        TEACHERS = "Преподаватели"
        JOIN_REQUESTS = "Заявки от учеников"
        SEND_JOIN_REQUEST = "Отправить заявку"
        PROFILE = "Мой профиль"
        EDIT = "Редактировать"
