from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.models.orm.lesson import Lesson


@dataclass
class LessonDTO:
    uuid_slot: UUID
    uuid_day: UUID
    t_username: str
    dt_start: datetime
    dt_add: datetime
    s_username: str | None = None
    id_lesson_type: int | None = None
    dt_spot: datetime | None = None

    @staticmethod
    def get_lesson_dto(lesson: Lesson):
        result_lesson = LessonDTO(
            uuid_slot=lesson.uuid_slot,
            uuid_day=lesson.uuid_day,
            t_username=lesson.t_username,
            dt_start=lesson.dt_start,
            dt_add=lesson.dt_add,
            s_username=lesson.s_username,
            id_lesson_type=lesson.id_lesson_type,
            dt_spot=lesson.dt_spot
        )
        return result_lesson
