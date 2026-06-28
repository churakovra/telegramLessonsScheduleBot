from datetime import UTC, date, datetime, time, timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.recurrence_repository import RecurrenceRepository
from app.repositories.slot_repository import SlotRepository
from app.schemas.recurrence import CreateRecurrenceRuleDTO, RecurrenceRuleDTO
from app.schemas.slot import CreateSlotDTO
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class RecurrenceService:
    def __init__(
        self,
        session: AsyncSession | None = None,
        repository: RecurrenceRepository | None = None,
        slot_repository: SlotRepository | None = None,
    ):
        if repository is None:
            if session is None:
                raise ValueError("RecurrenceService requires session or repository")
            repository = RecurrenceRepository(session)
        if slot_repository is None:
            if session is None:
                raise ValueError("RecurrenceService requires session or slot_repository")
            slot_repository = SlotRepository(session)
        self._repository = repository
        self._slot_repository = slot_repository

    async def create_rule(
        self,
        teacher_uuid: UUID,
        day_of_week: int,
        time_start: time,
        time_end: time,
        slot_duration: int,
        date_start: date,
        date_end: date,
    ) -> RecurrenceRuleDTO:
        rule = CreateRecurrenceRuleDTO(
            teacher_uuid=teacher_uuid,
            day_of_week=day_of_week,
            time_start=time_start,
            time_end=time_end,
            slot_duration_minutes=slot_duration,
            date_start=date_start,
            date_end=date_end,
        )
        return await self._repository.create_rule(rule)

    async def get_teacher_rules(self, teacher_uuid: UUID) -> list[RecurrenceRuleDTO]:
        return await self._repository.get_teacher_rules(teacher_uuid)

    async def delete_rule(self, uuid: UUID) -> None:
        await self._repository.delete_rule(uuid)

    async def materialize_slots(self) -> int:
        today = datetime.now(UTC).astimezone().date()
        horizon = today + timedelta(weeks=4)
        rules = await self._repository.get_active_rules()
        created_count = 0

        for rule in rules:
            start_at = datetime.combine(today, time.min)
            end_at = datetime.combine(horizon + timedelta(days=1), time.min)
            existing = await self._repository.get_existing_slot_starts(
                rule.teacher_uuid, start_at, end_at
            )
            slots = self._build_slots(rule, today, horizon, existing)
            if not slots:
                continue
            try:
                await self._slot_repository.add_slots(slots)
                created_count += len(slots)
            except Exception:
                logger.warning(
                    "Failed to materialize recurrence rule %s", rule.uuid, exc_info=True
                )
        return created_count

    @staticmethod
    def _build_slots(
        rule: RecurrenceRuleDTO,
        today: date,
        horizon: date,
        existing: set[datetime],
    ) -> list[CreateSlotDTO]:
        slots: list[CreateSlotDTO] = []
        current = max(today, rule.date_start)
        current += timedelta(days=(rule.day_of_week - current.weekday()) % 7)
        last_day = min(horizon, rule.date_end)

        while current <= last_day:
            slot_start = datetime.combine(current, rule.time_start)
            day_end = datetime.combine(current, rule.time_end)
            step = timedelta(minutes=rule.slot_duration_minutes)
            while slot_start + step <= day_end:
                if slot_start not in existing:
                    slots.append(
                        CreateSlotDTO(
                            uuid_teacher=rule.teacher_uuid,
                            dt_start=slot_start,
                            uuid_student=None,
                            dt_spot=None,
                        )
                    )
                    existing.add(slot_start)
                slot_start += step
            current += timedelta(days=7)
        return slots
