from datetime import datetime

from sqlalchemy import select

from app.database import SessionLocal

from app.models.orm.teacher import Teacher
from app.models.orm.student import Student
from app.models.orm.admin import Admin
from app.models.orm.user import User
from app.models.orm.lesson import Lesson
from app.models.orm.lesson_type import LessonType

from app.models.teacher_slot import Slot


class SlotsRepo:
    @staticmethod
    async def add_slots(slots: list[Slot]):
        teacher_username = slots[0].teacher

        with SessionLocal.begin() as session:
            teacher_stmt = select(Teacher).where(Teacher.username == teacher_username)
            teacher = session.scalar(teacher_stmt)
            if not teacher:
                print("no techa")
                return
            for slot in slots:
                for slot_dt in slot.available_time:
                    session.add(Lesson(teacher=teacher, dt_start=datetime.combine(slot.slot_date, slot_dt)))
