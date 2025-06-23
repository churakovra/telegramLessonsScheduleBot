from datetime import datetime
from uuid import uuid4, UUID

from sqlalchemy import select, update, func, and_
from sqlalchemy.orm import Session

from app.db.orm.lesson import Lesson
from app.db.orm import Teacher
from app.db.orm.slot import Slot
from app.schemas.lesson_dto import LessonDTO
from app.schemas.slot_dto import SlotDTO


class SlotRepository:
    def __init__(self, session: Session):
        self._db = session

    def add_slot(self, slot_dto: SlotDTO):
        slot = Slot.new_instance(slot_dto)
        self._db.add(slot)
        self._db.commit()
        self._db.refresh(slot)

    async def get_slots(self, uuid_day: UUID) -> list[LessonDTO]:
        res = list()
        stmt = select(Lesson).where(Lesson.uuid_day == uuid_day)
        lessons = await self._db.scalars(stmt)
        for lesson in lessons:
            lesson_dto = LessonDTO.get_lesson_dto(lesson)
            res.append(lesson_dto)
        return res

    def get_free_slots(self, teacher_uuid: UUID):
        slots = list()
        stmt = (
            select(Slot)
            .where(
                and_(
                    Slot.dt_add > func.now(),
                    Slot.uuid_student == None
                )
            )
        )
        for slot in self._db.scalars(stmt):
            slots.append(SlotDTO.to_dto(slot))


    async def get_slot(self, uuid_slot: UUID) -> LessonDTO:
        stmt = select(Lesson).where(Lesson.uuid_slot == uuid_slot)
        lesson = await self._db.scalar(stmt)
        lesson_dto = LessonDTO.get_lesson_dto(lesson)

        return lesson_dto

    async def assign_slot(self, slot: LessonDTO, s_username: str):
        stmt = (
            update(Lesson)
            .where(Lesson.uuid_slot == slot.uuid_slot)
            .values(s_username=s_username, dt_spot=datetime.now())
        )
        await self._db.execute(stmt)
