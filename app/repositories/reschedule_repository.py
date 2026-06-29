from datetime import datetime
from uuid import UUID

from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.orm.reschedule import RescheduleRequest
from app.database.orm.slot import Slot
from app.database.orm.user import User
from app.repositories.base import BaseRepository
from app.schemas.reschedule import (
    CreateRescheduleRequestDTO,
    RescheduleRequestDTO,
    RescheduleRequestInfoDTO,
)
from app.utils.datetime_utils import full_format_no_sec
from app.utils.enums.bot_values import RescheduleStatus


class RescheduleRepository(BaseRepository):
    def __init__(self, session: AsyncSession, *, auto_commit: bool = True):
        super().__init__(session, auto_commit=auto_commit)

    async def create_request(
        self, request_dto: CreateRescheduleRequestDTO
    ) -> RescheduleRequestDTO:
        request = RescheduleRequest(**request_dto.model_dump())
        return RescheduleRequestDTO.model_validate(await self.add(request))

    async def get_request(self, uuid: UUID) -> RescheduleRequestDTO | None:
        stmt = select(RescheduleRequest).where(RescheduleRequest.uuid == uuid)
        return await self.one_or_none_dto(stmt, RescheduleRequestDTO)

    async def get_pending_for_teacher(
        self, teacher_uuid: UUID
    ) -> list[RescheduleRequestInfoDTO]:
        stmt = (
            select(RescheduleRequest, User, Slot)
            .join(User, User.uuid == RescheduleRequest.student_uuid)
            .join(Slot, Slot.uuid == RescheduleRequest.slot_uuid)
            .where(
                RescheduleRequest.teacher_uuid == teacher_uuid,
                RescheduleRequest.status == RescheduleStatus.PENDING,
            )
            .order_by(RescheduleRequest.created_at.asc())
        )
        requests = []
        for request, student, slot in await self.session.execute(stmt):
            student_name = " ".join(
                part for part in [student.firstname, student.lastname] if part
            )
            requests.append(
                RescheduleRequestInfoDTO(
                    **RescheduleRequestDTO.model_validate(request).model_dump(),
                    student_name=student_name or student.username,
                    student_chat_id=student.chat_id,
                    original_dt_start=slot.dt_start.strftime(full_format_no_sec),
                )
            )
        return requests

    async def update_status(self, uuid: UUID, status: RescheduleStatus) -> None:
        stmt = (
            update(RescheduleRequest)
            .where(RescheduleRequest.uuid == uuid)
            .values(status=status)
        )
        await self.execute(stmt)

    async def move_slot(
        self,
        slot_uuid: UUID,
        teacher_uuid: UUID,
        student_uuid: UUID,
        dt_start: datetime,
    ) -> None:
        stmt = (
            update(Slot)
            .where(
                and_(
                    Slot.uuid == slot_uuid,
                    Slot.uuid_teacher == teacher_uuid,
                    Slot.uuid_student == student_uuid,
                )
            )
            .values(dt_start=dt_start)
        )
        await self.execute(stmt)
