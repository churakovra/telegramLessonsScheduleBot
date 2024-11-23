from datetime import datetime
from typing import override

from schedule_settings import ScheduleSettings
from date_time_utils import get_start_weekday, next_start_day


class Lesson:
    def __init__(self, lesson_date, lesson_time_start, lesson_type: int = 1):
        self.lesson_date = lesson_date
        self.lesson_time_start = lesson_time_start
        self.lesson_type = lesson_type


class Schedule(ScheduleSettings):
    def __init__(self, day):
        self.empty_schedule = self.__create_empty_schedule(day)

    def __fill_windows(self, curr_day: datetime):
        windows = []
        for w in range(self.AVAILABLE_LESSONS):
            t = curr_day.time()
            # TODO Убрать окно в 18:00. Вместо него 19:00 и дальше по логике
            windows.append(None)
            curr_day = curr_day + self.DURATION_1H + self.GAP
        return windows

    def __create_empty_schedule(self, day: datetime):
        schedule = {}
        curr_week_start = get_start_weekday(day)
        for day in range(self.WORK_DAYS):
            windows = self.__fill_windows(curr_week_start)
            schedule[curr_week_start.date()] = windows
            curr_week_start = next_start_day(curr_week_start)
        return schedule

    def get_vars(self):
        print(self.AVAILABLE_LESSONS, self.WORK_DAYS)










weekdays = {
    0: 'Понедельник',
    1: 'Вторник',
    2: 'Среда',
    3: 'Четверг',
    4: 'Пятница-развратница'
}

for values in weekdays.items():
    print(values[1])