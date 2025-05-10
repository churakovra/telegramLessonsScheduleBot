from datetime import datetime

from sqlalchemy import select

from app.models.teacher_slot import Slot

from app.database import SessionLocal
from app.models.admin import Admin
from app.models.teacher import Teacher
from app.models.student import Student
from app.models.user import User
from app.models.lesson_type import LessonType
from app.models.lesson import Lesson


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
