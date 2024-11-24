import calendar
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
