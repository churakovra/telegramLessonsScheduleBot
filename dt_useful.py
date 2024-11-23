import calendar
import pytz
from datetime import datetime, timedelta


full_format: str = '%d.%m.%Y %H:%M:%S'
day_format: str = '%d.%m.%Y'
time_format: str = '%H:%M:%S'

weekdays = {
    0: 'Понедельник',
    1: 'Вторник',
    2: 'Среда',
    3: 'Четверг',
    4: 'Пятница-развратница'
}


def is_first_week_day(day: datetime) -> bool:
    return day == calendar.firstweekday()


def which_day(day: datetime) -> int:
    wd = calendar.weekday(
        year=day.year,
        month=day.month,
        day=day.day,
    )
    return wd


def accurate_daytime(day: datetime) -> datetime:
    day = day.replace(hour=10, minute=0, second=0, microsecond=0)
    return day


def next_start_day(day: datetime) -> datetime:
    next_day = day + timedelta(days=1)
    next_day = accurate_daytime(next_day)
    return next_day


def get_day_schedule(day_callback: str):
    weekday: int = int(day_callback[len(day_callback) - 1])
    day: datetime = get_datetime_from_weekday(weekday)
    lessons = get_day_lessons(day)
    schedule = get_schedule(lessons)

def get_schedule(lessons: list[datetime]) -> list[datetime]:
    pass


def get_datetime_from_weekday(weekday: int) -> datetime:
    cday = datetime.now()
    ccal = which_day(cday)
    if weekday > 6:
        raise Exception
    if ccal <= 4:
        # Получаем дату для дня на этой неделе
        day = cday + timedelta(days=weekday - ccal)
        return day
    else:
        # Получаем дату для дня на следующей неделе
        day = cday + timedelta(weekday + 1)
        if ccal == 5:
            day += timedelta(1)
        return day


def get_day_lessons(day: datetime) -> list[datetime]:
    # TODO get from dp lessons for day
    pass



ccal = calendar.weekday(datetime.now().year, datetime.now().month, datetime.now().day)
print(ccal)