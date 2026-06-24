from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import and_, delete, extract, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.orm.slot import Slot
from app.repositories.base import BaseRepository
from app.schemas.slot import CreateSlotDTO, SlotDTO


class SlotRepository(BaseRepository):
    def __init__(self, session: AsyncSession, *, auto_commit: bool = True):
        super().__init__(session, auto_commit=auto_commit)

    async def add_slots(self, slots_dto: list[CreateSlotDTO]) -> None:
        slots = [Slot(**slot.model_dump()) for slot in slots_dto]
        await self.add_many(slots)

    async def get_slot(self, slot_uuid: UUID) -> SlotDTO | None:
        stmt = select(Slot).where(Slot.uuid == slot_uuid)
        return await self.one_or_none_dto(stmt, SlotDTO)

    async def get_slots(
        self, teacher_uuid: UUID, week: int | None = None
    ) -> list[SlotDTO]:
        conditions = [Slot.uuid_teacher == teacher_uuid]
        if week is not None:
            conditions.append(extract("week", Slot.dt_start) == week)

        stmt = select(Slot).where(and_(*conditions)).order_by(Slot.dt_start.asc())
        return await self.list_dto(stmt, SlotDTO)

    async def get_free_slots(self, teacher_uuid: UUID) -> list[SlotDTO]:
        stmt = (
            select(Slot)
            .where(
                and_(
                    Slot.uuid_teacher == teacher_uuid,
                    Slot.dt_start > func.now(),
                    Slot.uuid_student.is_(None),
                )
            )
            .order_by(Slot.dt_start.asc())
        )
        return await self.list_dto(stmt, SlotDTO)

    async def get_day_free_slots(
        self, day: datetime, teacher_uuid: UUID
    ) -> list[SlotDTO]:
        stmt = (
            select(Slot)
            .where(
                and_(
                    func.date(Slot.dt_start) == day.date(),
                    Slot.uuid_teacher == teacher_uuid,
                    Slot.uuid_student.is_(None),
                )
            )
            .order_by(Slot.dt_start.asc())
        )
        return await self.list_dto(stmt, SlotDTO)

    async def assign_slot(self, student_uuid: UUID, slot_uuid: UUID) -> None:
        stmt = (
            update(Slot)
            .where(Slot.uuid == slot_uuid)
            .values(uuid_student=student_uuid, dt_spot=datetime.now(UTC).astimezone())
        )
        await self.execute(stmt)

    async def delete_slots(self, slots: list[SlotDTO]) -> None:
        if not slots:
            return

        stmt = delete(Slot).where(Slot.uuid.in_([slot.uuid for slot in slots]))
        await self.execute(stmt)

    async def delete_slots_attached_to_student(self, student_uuid: UUID) -> None:
        stmt = delete(Slot).where(Slot.uuid_student == student_uuid)
        await self.execute(stmt)

    async def delete_slot(self, slot_uuid: UUID) -> None:
        stmt = delete(Slot).where(Slot.uuid == slot_uuid)
        await self.execute(stmt)
