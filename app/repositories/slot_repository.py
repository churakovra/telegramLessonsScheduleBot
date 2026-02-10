from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import and_, delete, extract, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.orm.slot import Slot
from app.schemas.slot_dto import CreateSlotDTO, SlotDTO


class SlotRepository:
    def __init__(self, session: AsyncSession):
        self._db = session

    async def add_slots(self, slots_dto: list[CreateSlotDTO]):
        slots = [Slot(**slot.model_dump()) for slot in slots_dto]
        self._db.add_all(slots)
        await self._db.commit()

    async def get_slot(self, slot_uuid: UUID):
        stmt = select(Slot).where(Slot.uuid == slot_uuid)
        slot = await self._db.scalar(stmt)
        if slot is None:
            return slot
        return SlotDTO.model_validate(slot)

    async def get_slots(
        self, teacher_uuid: UUID, week: int | None = None
    ) -> list[SlotDTO]:
        slots = list()
        stmt = (
            select(Slot)
            .where(
                and_(
                    Slot.uuid_teacher == teacher_uuid,
                    extract("week", Slot.dt_start) == week,
                )
            )
            .order_by(Slot.dt_start.asc())
        )
        for slot in await self._db.scalars(stmt):
            slots.append(SlotDTO.model_validate(slot))
        return slots

    async def get_free_slots(self, teacher_uuid: UUID) -> list[SlotDTO]:
        slots = list()
        stmt = select(Slot).where(
            and_(
                Slot.uuid_teacher == teacher_uuid,
                Slot.dt_start > func.now(),
                Slot.uuid_student.is_(None),
            )
        )
        for slot in await self._db.scalars(stmt):
            slots.append(SlotDTO.model_validate(slot))
        return slots

    async def get_day_free_slots(
        self, day: datetime, teacher_uuid: UUID
    ) -> list[SlotDTO]:
        slots = list()
        stmt = select(Slot).where(
            and_(
                func.date(Slot.dt_start) == day,
                Slot.uuid_teacher == teacher_uuid,
                Slot.uuid_student.is_(None),
            )
        )
        for slot in await self._db.scalars(stmt):
            slots.append(SlotDTO.model_validate(slot))
        return slots

    async def assign_slot(self, student_uuid: UUID, slot_uuid: UUID):
        stmt = (
            update(Slot)
            .where(Slot.uuid == slot_uuid)
            .values(uuid_student=student_uuid)
            .values(dt_spot=datetime.now(UTC).astimezone())
        )
        await self._db.execute(stmt)
        await self._db.commit()

    async def delete_slots(self, slots: list[SlotDTO]):
        stmt = delete(Slot).where(Slot.uuid.in_([slot.uuid for slot in slots]))
        await self._db.execute(stmt)
        await self._db.commit()

    async def delete_slots_attached_to_student(self, student_uuid: UUID):
        stmt = delete(Slot).where(Slot.uuid_student == student_uuid)
        await self._db.execute(stmt)
        await self._db.commit()

    async def delete_slot(self, slot_uuid: UUID) -> None:
        stmt = delete(Slot).where(Slot.uuid == slot_uuid)
        await self._db.execute(stmt)
        await self._db.commit()
