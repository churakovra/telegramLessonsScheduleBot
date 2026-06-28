from datetime import datetime
from uuid import UUID

from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.orm.recurrence import RecurrenceRule
from app.database.orm.slot import Slot
from app.repositories.base import BaseRepository
from app.schemas.recurrence import CreateRecurrenceRuleDTO, RecurrenceRuleDTO


class RecurrenceRepository(BaseRepository):
    def __init__(self, session: AsyncSession, *, auto_commit: bool = True):
        super().__init__(session, auto_commit=auto_commit)

    async def create_rule(
        self, rule_dto: CreateRecurrenceRuleDTO
    ) -> RecurrenceRuleDTO:
        rule = RecurrenceRule(**rule_dto.model_dump())
        return RecurrenceRuleDTO.model_validate(await self.add(rule))

    async def get_teacher_rules(self, teacher_uuid: UUID) -> list[RecurrenceRuleDTO]:
        stmt = (
            select(RecurrenceRule)
            .where(RecurrenceRule.teacher_uuid == teacher_uuid)
            .order_by(RecurrenceRule.day_of_week.asc(), RecurrenceRule.time_start.asc())
        )
        return await self.list_dto(stmt, RecurrenceRuleDTO)

    async def get_active_rules(self) -> list[RecurrenceRuleDTO]:
        stmt = select(RecurrenceRule).where(RecurrenceRule.is_active.is_(True))
        return await self.list_dto(stmt, RecurrenceRuleDTO)

    async def delete_rule(self, uuid: UUID) -> None:
        stmt = delete(RecurrenceRule).where(RecurrenceRule.uuid == uuid)
        await self.execute(stmt)

    async def get_existing_slot_starts(
        self, teacher_uuid: UUID, start_at: datetime, end_at: datetime
    ) -> set[datetime]:
        stmt = select(Slot.dt_start).where(
            and_(
                Slot.uuid_teacher == teacher_uuid,
                Slot.dt_start >= start_at,
                Slot.dt_start < end_at,
            )
        )
        return set(await self.session.scalars(stmt))
