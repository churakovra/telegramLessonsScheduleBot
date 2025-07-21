from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, func, and_, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_only

from app.db.orm.slot import Slot
from app.schemas.slot_dto import SlotDTO


class SlotRepository:
    def __init__(self, session: AsyncSession):
        self._db = session

    async def add_slot(self, slot_dto: SlotDTO):
        slot = Slot.new_instance(slot_dto)
        try:
            self._db.add(slot)
            await self._db.commit()
            await self._db.refresh(slot)
        except IntegrityError as e:
            await self._db.rollback()
            raise ValueError(e) from e

    async def get_slot(self, slot_uuid: UUID):
        stmt = select(Slot).where(Slot.uuid == slot_uuid)
        slot = await self._db.scalar(stmt)
        if slot is None:
            return slot
        slot_dto = SlotDTO(
            uuid=slot.uuid,
            uuid_teacher=slot.uuid_teacher,
            dt_start=slot.dt_start,
            dt_add=slot.dt_add,
            uuid_student=slot.uuid_student,
            dt_spot=slot.dt_spot
        )
        return slot_dto

    async def get_free_slots(self, teacher_uuid: UUID) -> list[SlotDTO]:
        slots = list()
        stmt = (
            select(Slot)
            .where(
                and_(
                    Slot.uuid_teacher == teacher_uuid,
                    Slot.dt_start > func.now(),
                    Slot.uuid_student == None
                )
            )
        )
        for slot in await self._db.scalars(stmt):
            slot_dto = SlotDTO(
                uuid=slot.uuid,
                uuid_teacher=slot.uuid_teacher,
                dt_start=slot.dt_start,
                dt_add=slot.dt_add,
                uuid_student=slot.uuid_student,
                dt_spot=slot.dt_spot
            )
            slots.append(slot_dto)
        return slots

    async def get_day_slots(self, day: datetime, teacher_uuid: UUID) -> list[SlotDTO]:
        slots = list()
        stmt = (
            select(Slot)
            .where(
                and_(
                    func.date(Slot.dt_start) == day,
                    Slot.uuid_teacher == teacher_uuid,
                    Slot.uuid_student == None
                )
            )
        )
        for slot in await self._db.scalars(stmt):
            slot_dto = SlotDTO(
                uuid=slot.uuid,
                uuid_teacher=slot.uuid_teacher,
                dt_start=slot.dt_start,
                dt_add=slot.dt_add,
                uuid_student=slot.uuid_student,
                dt_spot=slot.dt_spot
            )
            slots.append(slot_dto)
        return slots

    async def assign_slot(self, student_uuid: UUID, slot_uuid: UUID):
        stmt = (
            update(Slot)
            .where(Slot.uuid == slot_uuid)
            .values(uuid_student=student_uuid)
            .values(dt_spot=datetime.now(timezone.utc).astimezone())
        )
        await self._db.execute(stmt)
        await self._db.commit()
