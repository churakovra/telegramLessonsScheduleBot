from datetime import timedelta


class ScheduleSettings:
    DURATION_1H = timedelta(hours=1)
    DURATION_1H30M = timedelta(hours=1.5)
    GAP = timedelta(minutes=10)
    WORK_DAYS: int = 5
    AVAILABLE_LESSONS = 9
