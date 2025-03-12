from datetime import datetime
from utils.datetime_utils import h1, m10, accurate_daytime
from gap import Gap
from lesson import Lesson
from schedule_settings import ScheduleSettings
from schedule_db import get_lessons


class Schedule(ScheduleSettings):
    def __init__(self, cday: datetime):
        self.__schedule = self._create_schedule(cday)

    def get_schedule(self) -> list[Lesson | Gap]:
        if self.__schedule is not None:
            return self.__schedule

    @staticmethod
    def _create_schedule(cday: datetime) -> list[Lesson | Gap]:
        schedule = []
        lessons = get_lessons(cday)
        dt_st = accurate_daytime(cday)
        for i in range(0, Schedule.AVAILABLE_LESSONS):
            dt_end = dt_st + h1
            gap = Gap(
                number=i,
                datetime_start=dt_st,
                datetime_end=dt_end
            )
            if i == 6:
                dt_st = dt_end + h1
            else:
                dt_st = dt_end + m10
            schedule.append(gap)

        if len(lessons) > 0:
            for gap in schedule:
                for lesson in lessons:
                    if lesson.datetime_start == gap.datetime_start:
                        schedule[schedule.index(gap)] = lesson
        return schedule


"""
    def __create_week_schedule(self, cday: datetime):
        schedule = {}
        csday = curr_start_day(cday)
        for day in range(self.WORK_DAYS):
            gaps = self.__fill_gaps(csday)
            schedule[csday.date()] = gaps
            csday = next_start_day(csday)
        return schedule
"""
