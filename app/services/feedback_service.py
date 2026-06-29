from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.slot_repository import SlotRepository
from app.schemas.feedback import (
    CreateFeedbackDTO,
    FeedbackDTO,
    FeedbackInfoDTO,
    FeedbackPromptDTO,
)
from app.utils.enums.bot_values import StatisticsPeriod
from app.utils.exceptions.slot_exceptions import SlotNotFoundException


@dataclass(frozen=True)
class FeedbackSummary:
    average_rating: float
    feedback: list[FeedbackInfoDTO]


class FeedbackService:
    def __init__(
        self,
        session: AsyncSession | None = None,
        repository: FeedbackRepository | None = None,
        slot_repository: SlotRepository | None = None,
    ):
        if repository is None:
            if session is None:
                raise ValueError("FeedbackService requires session or repository")
            repository = FeedbackRepository(session)
        if slot_repository is None:
            if session is None:
                raise ValueError("FeedbackService requires session or slot_repository")
            slot_repository = SlotRepository(session)
        self._repository = repository
        self._slot_repository = slot_repository

    async def submit_feedback(
        self,
        slot_uuid: UUID,
        student_uuid: UUID,
        rating: int,
        comment: str | None,
    ) -> FeedbackDTO:
        slot = await self._slot_repository.get_slot(slot_uuid)
        if slot is None or slot.uuid_student != student_uuid:
            raise SlotNotFoundException(slot_uuid)
        existing = await self._repository.get_feedback_by_slot(slot_uuid)
        if existing is not None:
            return existing
        feedback = CreateFeedbackDTO(
            slot_uuid=slot_uuid,
            student_uuid=student_uuid,
            teacher_uuid=slot.uuid_teacher,
            rating=rating,
            comment=comment,
        )
        return await self._repository.create_feedback(feedback)

    async def get_teacher_feedback(
        self, teacher_uuid: UUID, period: StatisticsPeriod
    ) -> FeedbackSummary:
        start_at, end_at = self._period_bounds(period)
        feedback = await self._repository.get_teacher_feedback(
            teacher_uuid, start_at, end_at
        )
        average = (
            round(sum(item.rating for item in feedback) / len(feedback), 2)
            if feedback
            else 0
        )
        return FeedbackSummary(average_rating=average, feedback=feedback)

    async def get_slots_waiting_feedback_prompt(self) -> list[FeedbackPromptDTO]:
        return await self._repository.get_slots_waiting_feedback_prompt(
            datetime.now(UTC).astimezone()
        )

    async def mark_feedback_prompt_sent(self, slot_uuid: UUID) -> None:
        await self._repository.mark_feedback_prompt_sent(slot_uuid)

    @staticmethod
    def _period_bounds(period: StatisticsPeriod) -> tuple[datetime, datetime]:
        now = datetime.now(UTC).astimezone()
        if period == StatisticsPeriod.WEEK:
            start_at = now.replace(
                hour=0, minute=0, second=0, microsecond=0
            ) - timedelta(days=now.weekday())
            return start_at, start_at + timedelta(days=7)
        if period == StatisticsPeriod.MONTH:
            start_at = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if start_at.month == 12:
                return start_at, start_at.replace(year=start_at.year + 1, month=1)
            return start_at, start_at.replace(month=start_at.month + 1)
        start_at = now.replace(
            month=1, day=1, hour=0, minute=0, second=0, microsecond=0
        )
        return start_at, start_at.replace(year=start_at.year + 1)
