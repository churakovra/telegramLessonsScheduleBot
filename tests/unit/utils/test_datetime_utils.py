import calendar
from datetime import datetime

import pytest

from app.utils.datetime_utils import (
    accurate_daytime,
    curr_start_day,
    get_datetime_from_weekday,
    next_start_day,
    which_day,
)


def test_which_day_returns_calendar_weekday():
    assert which_day(datetime(2026, 6, 22)) == calendar.MONDAY


def test_accurate_daytime_sets_ten_am():
    result = accurate_daytime(datetime(2026, 6, 23, 18, 45, 12, 123))

    assert result == datetime(2026, 6, 23, 10)


def test_curr_start_day_returns_monday_at_ten():
    result = curr_start_day(datetime(2026, 6, 25, 18))

    assert result == datetime(2026, 6, 22, 10)


def test_next_start_day_returns_next_calendar_day_at_ten():
    result = next_start_day(datetime(2026, 6, 25, 18))

    assert result == datetime(2026, 6, 26, 10)


@pytest.mark.parametrize(
    ("current", "weekday", "expected"),
    [
        (datetime(2026, 6, 22, 10), calendar.FRIDAY, datetime(2026, 6, 26, 10)),
        (datetime(2026, 6, 27, 10), calendar.MONDAY, datetime(2026, 6, 29, 10)),
        (datetime(2026, 6, 28, 10), calendar.FRIDAY, datetime(2026, 7, 3, 10)),
    ],
)
def test_get_datetime_from_weekday(current, weekday, expected):
    assert get_datetime_from_weekday(weekday, current) == expected


@pytest.mark.parametrize("weekday", [-1, calendar.SATURDAY, calendar.SUNDAY])
def test_get_datetime_from_weekday_rejects_weekends_and_invalid_values(weekday):
    with pytest.raises(Exception):
        get_datetime_from_weekday(weekday, datetime(2026, 6, 22))
