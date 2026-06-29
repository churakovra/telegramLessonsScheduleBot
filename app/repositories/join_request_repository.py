from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.orm.join_request import JoinRequest
from app.database.orm.user import User
from app.repositories.base import BaseRepository
from app.schemas.join_request import (
    CreateJoinRequestDTO,
    JoinRequestDTO,
    JoinRequestInfoDTO,
)
from app.utils.enums.bot_values import JoinRequestStatus


class JoinRequestRepository(BaseRepository):
    def __init__(self, session: AsyncSession, *, auto_commit: bool = True):
        super().__init__(session, auto_commit=auto_commit)

    async def create_request(self, request_dto: CreateJoinRequestDTO) -> JoinRequestDTO:
        request = JoinRequest(**request_dto.model_dump())
        return JoinRequestDTO.model_validate(await self.add(request))

    async def get_request(self, uuid: UUID) -> JoinRequestDTO | None:
        stmt = select(JoinRequest).where(JoinRequest.uuid == uuid)
        return await self.one_or_none_dto(stmt, JoinRequestDTO)

    async def get_for_pair(
        self, student_uuid: UUID, teacher_uuid: UUID
    ) -> JoinRequestDTO | None:
        stmt = select(JoinRequest).where(
            JoinRequest.student_uuid == student_uuid,
            JoinRequest.teacher_uuid == teacher_uuid,
        )
        return await self.one_or_none_dto(stmt, JoinRequestDTO)

    async def get_pending_for_teacher(
        self, teacher_uuid: UUID
    ) -> list[JoinRequestInfoDTO]:
        stmt = (
            select(JoinRequest, User)
            .join(User, User.uuid == JoinRequest.student_uuid)
            .where(
                JoinRequest.teacher_uuid == teacher_uuid,
                JoinRequest.status == JoinRequestStatus.PENDING,
            )
            .order_by(JoinRequest.created_at.asc())
        )
        requests = []
        for request, student in await self.session.execute(stmt):
            requests.append(
                JoinRequestInfoDTO(
                    **JoinRequestDTO.model_validate(request).model_dump(),
                    student_username=student.username,
                    student_firstname=student.firstname,
                    student_lastname=student.lastname,
                    student_chat_id=student.chat_id,
                )
            )
        return requests

    async def count_pending_for_teacher(self, teacher_uuid: UUID) -> int:
        stmt = select(JoinRequest).where(
            JoinRequest.teacher_uuid == teacher_uuid,
            JoinRequest.status == JoinRequestStatus.PENDING,
        )
        return len(await self.scalars(stmt))

    async def update_status(self, uuid: UUID, status: JoinRequestStatus) -> None:
        stmt = (
            update(JoinRequest)
            .where(JoinRequest.uuid == uuid)
            .values(status=status)
        )
        await self.execute(stmt)
