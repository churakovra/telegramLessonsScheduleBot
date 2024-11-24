from attr import dataclass


@dataclass
class Lesson:
    t_username: str
    s_username: str
    datetime_start: str
    datetime_end: str
    lesson_type: int = 0
