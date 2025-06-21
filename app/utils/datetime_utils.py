import calendar
from datetime import datetime, timedelta

full_format: str = '%d.%m.%Y %H:%M:%S'
full_format_no_sec: str = '%d.%m.%Y %H:%M'
day_format: str = '%d.%m.%Y'
day_format_db: str = '_%d.%m.%Y_'
time_format: str = '%H:%M:%S'
time_format_HM: str = '%H:%M'

h1 = timedelta(hours=1)
h1_5 = timedelta(hours=1, minutes=30)
m10 = timedelta(minutes=10)
m30 = timedelta(minutes=30)

WEEKDAYS = {
    0: ["Monday", "monday", "Понедельник",  "понедельник", "пн", "пнд"],
    1: ["Tuesday", "tuesday", "Вторник", "вторник", "вт"],
    2: ["Wednesday", "wednesday", "Среда", "среда", "ср"],
    3: ["Thursday", "thursday", "Четверг", "четверг", "чт"],
    4: ["Friday", "friday", "Пятница", "пятница", "пт"]
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


def curr_start_day(day: datetime) -> datetime:
    wd = which_day(day)
    start_day = day - timedelta(days=wd)
    start_day = accurate_daytime(start_day)
    return start_day


def next_start_day(day: datetime) -> datetime:
    next_day = day + timedelta(days=1)
    next_day = accurate_daytime(next_day)
    return next_day


def get_datetime_from_weekday(weekday: int, cday: datetime) -> datetime:
    ccal = which_day(cday)
    if weekday > calendar.FRIDAY or weekday < calendar.MONDAY:
        raise Exception
    if ccal <= calendar.FRIDAY:
        # Получаем дату для дня на этой неделе
        day = cday + timedelta(days=weekday - ccal)
        return day
    else:
        # Получаем дату для дня на следующей неделе
        day = cday + timedelta(weekday + 1)
        if ccal == calendar.SATURDAY:
            day += timedelta(1)
        return day
