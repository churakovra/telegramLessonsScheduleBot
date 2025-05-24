from uuid import uuid4, UUID
from datetime import datetime

from sqlalchemy import select, update

from app.database import SessionLocal
from app.models.lesson_dto import LessonDTO

from app.models.orm.teacher import Teacher
from app.models.orm.student import Student
from app.models.orm.admin import Admin
from app.models.orm.user import User
from app.models.orm.lesson import Lesson
from app.models.orm.lesson_type import LessonType

from app.models.teacher_slot import Slot


class SlotsRepo:
    @staticmethod
    async def add_slots(slots: list[Slot]) -> dict[str, UUID]:
        teacher_username = slots[0].teacher
        days = dict()
        with SessionLocal.begin() as session:
            teacher_stmt = select(Teacher).where(Teacher.username == teacher_username)
            teacher = session.scalar(teacher_stmt)
            if not teacher:
                raise Exception("no techa")
            for slot in slots:
                uuid_day = uuid4()
                days[slot.day_name] = uuid_day
                for slot_dt in slot.available_time:
                    uuid_slot = uuid4()
                    session.add(
                        Lesson(
                            uuid_slot=uuid_slot,
                            uuid_day=uuid_day,
                            t_username=teacher.username,
                            dt_start=datetime.combine(slot.slot_date, slot_dt)
                        )
                    )
        return days

    @staticmethod
    async def get_slots(uuid_day: UUID) -> list[LessonDTO]:
        res = list()
        with SessionLocal.begin() as session:
            stmt = select(Lesson).where(Lesson.uuid_day == uuid_day)
            lessons = session.scalars(stmt).all()
            for lesson in lessons:
                lesson_dto = LessonDTO.get_lesson_dto(lesson)
                res.append(lesson_dto)
        return res

    @staticmethod
    async def get_slot(uuid_slot: UUID) -> LessonDTO:
        stmt = select(Lesson).where(Lesson.uuid_slot == uuid_slot)
        with SessionLocal.begin() as session:
            lesson = session.scalar(stmt)
            lesson_dto = LessonDTO.get_lesson_dto(lesson)
        return lesson_dto

    @staticmethod
    async def assign_slot(slot: LessonDTO, s_username: str):
        stmt = (
            update(Lesson)
            .where(Lesson.uuid_slot == slot.uuid_slot)
            .values(s_username=s_username, dt_spot=datetime.now())
        )
        with SessionLocal.begin() as session:
            session.execute(stmt)
