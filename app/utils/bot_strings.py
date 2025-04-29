from dataclasses import dataclass


@dataclass
class BotStrings:
    GREETING: str = "Привет! Я Дианусик Гудлаки, твой преподаватель английского✨ Нажми на кнопку и запишись на урок 🤌"
    WEEKDAY: str = "Выбери день недели:"
    DAY_LESSONS: str = "Выбери время из доступного:"
    DURATION: str = "Выбери продолжительность урока:"
    APPROVE_ASK: str = "Подтверди запись 🤗"
    APPROVE_ANSW: str = "Подтверждаю 🙂‍↕️"
    BRANCH_DAYS: str = "Выбрать день"
    BRANCH_MANUAL: str = "Записаться вручную"
    SET_MANUAL: str = "Введи желаемое время из доступного, в формате 'Дата Время', например: '24.10.2024 12:30'"

    CALLBACK_BRANCH_DAYS: str = 'branch_days'
    CALLBACK_BRANCH_MANUAL: str = 'branch_manual'

    CALLBACK_DAY_0: str = "day_0"
    CALLBACK_DAY_1: str = "day_1"
    CALLBACK_DAY_2: str = "day_2"
    CALLBACK_DAY_3: str = "day_3"
    CALLBACK_DAY_4: str = "day_4"

    PARSING_SLOTS_PROCESSING: str = "Получил, обрабатываю"
    PARSING_SLOTS_SUCCESS: str = "Обработал!"


    YES: str = "Да"
    NO: str = "Нет"

    CALLBACK_SLOTS_CORRECT: str = "slots_correct"
    CALLBACK_SLOTS_INCORRECT: str = "slots_incorrect"

    SLOTS_SUCCESS_ANSWER: str = "Отлично! Отправил окошки ученикам 🤝"
    SLOTS_FAILURE_ANSWER: str = "Отправьте окошки еще раз"


bot_strings = BotStrings()
