from datetime import datetime

from attr import dataclass


@dataclass
class Lesson:
    t_username: str
    s_username: str
    datetime_start: datetime
    datetime_end: datetime
    lesson_type: int = 0
