from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.orm.feedback import Feedback
from app.database.orm.lesson import Lesson
from app.database.orm.slot import Slot
from app.database.orm.teacher_student import TeacherStudent
from app.database.orm.user import User
from app.repositories.base import BaseRepository
from app.schemas.feedback import (
    CreateFeedbackDTO,
    FeedbackDTO,
    FeedbackInfoDTO,
    FeedbackPromptDTO,
)


class FeedbackRepository(BaseRepository):
    def __init__(self, session: AsyncSession, *, auto_commit: bool = True):
        super().__init__(session, auto_commit=auto_commit)

    async def create_feedback(self, feedback_dto: CreateFeedbackDTO) -> FeedbackDTO:
        feedback = Feedback(**feedback_dto.model_dump())
        return FeedbackDTO.model_validate(await self.add(feedback))

    async def get_feedback_by_slot(self, slot_uuid: UUID) -> FeedbackDTO | None:
        stmt = select(Feedback).where(Feedback.slot_uuid == slot_uuid)
        return await self.one_or_none_dto(stmt, FeedbackDTO)

    async def get_teacher_feedback(
        self, teacher_uuid: UUID, start_at: datetime, end_at: datetime
    ) -> list[FeedbackInfoDTO]:
        stmt = (
            select(Feedback, User, Slot)
            .join(User, User.uuid == Feedback.student_uuid)
            .join(Slot, Slot.uuid == Feedback.slot_uuid)
            .where(
                Feedback.teacher_uuid == teacher_uuid,
                Feedback.created_at >= start_at,
                Feedback.created_at < end_at,
            )
            .order_by(Feedback.created_at.desc())
        )
        feedback = []
        for item, student, slot in await self.session.execute(stmt):
            student_name = " ".join(
                part for part in [student.firstname, student.lastname] if part
            )
            feedback.append(
                FeedbackInfoDTO(
                    **FeedbackDTO.model_validate(item).model_dump(),
                    student_name=student_name or student.username,
                    slot_time=slot.dt_start,
                )
            )
        return feedback

    async def get_slots_waiting_feedback_prompt(
        self, now: datetime
    ) -> list[FeedbackPromptDTO]:
        stmt = (
            select(Slot, User, Lesson)
            .join(User, User.uuid == Slot.uuid_student)
            .outerjoin(
                TeacherStudent,
                and_(
                    TeacherStudent.uuid_teacher == Slot.uuid_teacher,
                    TeacherStudent.uuid_student == Slot.uuid_student,
                ),
            )
            .outerjoin(Lesson, Lesson.uuid == TeacherStudent.uuid_lesson)
            .outerjoin(Feedback, Feedback.slot_uuid == Slot.uuid)
            .where(
                Slot.uuid_student.is_not(None),
                Slot.dt_spot.is_not(None),
                Slot.feedback_prompt_sent_at.is_(None),
                Feedback.uuid.is_(None),
            )
        )
        prompts = []
        for slot, student, lesson in await self.session.execute(stmt):
            duration = lesson.duration if lesson else 60
            end_at = slot.dt_start.replace(tzinfo=now.tzinfo) + _minutes(duration)
            if end_at > now:
                continue
            prompts.append(
                FeedbackPromptDTO(
                    slot_uuid=slot.uuid,
                    student_uuid=slot.uuid_student,
                    teacher_uuid=slot.uuid_teacher,
                    student_chat_id=student.chat_id,
                    dt_start=slot.dt_start,
                )
            )
        return prompts

    async def mark_feedback_prompt_sent(self, slot_uuid: UUID) -> None:
        stmt = (
            update(Slot)
            .where(Slot.uuid == slot_uuid)
            .values(feedback_prompt_sent_at=datetime.now(UTC).astimezone())
        )
        await self.execute(stmt)


def _minutes(value: int):
    from datetime import timedelta

    return timedelta(minutes=value)
