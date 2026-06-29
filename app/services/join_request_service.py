from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.join_request_repository import JoinRequestRepository
from app.repositories.teacher_repository import TeacherRepository
from app.schemas.join_request import (
    CreateJoinRequestDTO,
    JoinRequestDTO,
    JoinRequestInfoDTO,
)
from app.utils.enums.bot_values import JoinRequestStatus


class JoinRequestService:
    def __init__(
        self,
        session: AsyncSession | None = None,
        repository: JoinRequestRepository | None = None,
        teacher_repository: TeacherRepository | None = None,
    ):
        if repository is None:
            if session is None:
                raise ValueError("JoinRequestService requires session or repository")
            repository = JoinRequestRepository(session)
        if teacher_repository is None:
            if session is None:
                raise ValueError(
                    "JoinRequestService requires session or teacher_repository"
                )
            teacher_repository = TeacherRepository(session)
        self._repository = repository
        self._teacher_repository = teacher_repository

    async def create_request(
        self, student_uuid: UUID, teacher_uuid: UUID
    ) -> JoinRequestDTO:
        existing = await self._repository.get_for_pair(student_uuid, teacher_uuid)
        if existing is not None:
            raise ValueError("Join request already exists")
        request = CreateJoinRequestDTO(
            student_uuid=student_uuid,
            teacher_uuid=teacher_uuid,
        )
        return await self._repository.create_request(request)

    async def get_pending_for_teacher(
        self, teacher_uuid: UUID
    ) -> list[JoinRequestInfoDTO]:
        return await self._repository.get_pending_for_teacher(teacher_uuid)

    async def count_pending_for_teacher(self, teacher_uuid: UUID) -> int:
        return await self._repository.count_pending_for_teacher(teacher_uuid)

    async def get_request(self, uuid: UUID) -> JoinRequestDTO:
        request = await self._repository.get_request(uuid)
        if request is None:
            raise ValueError(f"Join request {uuid} not found")
        return request

    async def approve(self, uuid: UUID) -> JoinRequestDTO:
        request = await self.get_request(uuid)
        if request.status != JoinRequestStatus.PENDING:
            raise ValueError("Join request is already processed")
        try:
            await self._teacher_repository.attach_student(
                request.teacher_uuid,
                request.student_uuid,
                uuid_lesson=None,
            )
        except ValueError:
            pass
        await self._repository.update_status(uuid, JoinRequestStatus.APPROVED)
        return request

    async def reject(self, uuid: UUID) -> JoinRequestDTO:
        request = await self.get_request(uuid)
        if request.status != JoinRequestStatus.PENDING:
            raise ValueError("Join request is already processed")
        await self._repository.update_status(uuid, JoinRequestStatus.REJECTED)
        return request
