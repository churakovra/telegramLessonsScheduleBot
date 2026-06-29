from datetime import date, datetime, time
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.reschedule_repository import RescheduleRepository
from app.repositories.slot_repository import SlotRepository
from app.schemas.reschedule import (
    CreateRescheduleRequestDTO,
    RescheduleRequestDTO,
    RescheduleRequestInfoDTO,
)
from app.utils.enums.bot_values import RescheduleStatus
from app.utils.exceptions.slot_exceptions import SlotNotFoundException


class RescheduleService:
    def __init__(
        self,
        session: AsyncSession | None = None,
        repository: RescheduleRepository | None = None,
        slot_repository: SlotRepository | None = None,
    ):
        if repository is None:
            if session is None:
                raise ValueError("RescheduleService requires session or repository")
            repository = RescheduleRepository(session)
        if slot_repository is None:
            if session is None:
                raise ValueError("RescheduleService requires session or slot_repository")
            slot_repository = SlotRepository(session)
        self._repository = repository
        self._slot_repository = slot_repository

    async def create_request(
        self,
        student_uuid: UUID,
        slot_uuid: UUID,
        requested_date: date,
        requested_time: time,
    ) -> RescheduleRequestDTO:
        slot = await self._slot_repository.get_slot(slot_uuid)
        if slot is None or slot.uuid_student != student_uuid:
            raise SlotNotFoundException(slot_uuid)
        request = CreateRescheduleRequestDTO(
            slot_uuid=slot_uuid,
            student_uuid=student_uuid,
            teacher_uuid=slot.uuid_teacher,
            requested_date=requested_date,
            requested_time=requested_time,
        )
        return await self._repository.create_request(request)

    async def get_pending_for_teacher(
        self, teacher_uuid: UUID
    ) -> list[RescheduleRequestInfoDTO]:
        return await self._repository.get_pending_for_teacher(teacher_uuid)

    async def get_request(self, uuid: UUID) -> RescheduleRequestDTO:
        request = await self._repository.get_request(uuid)
        if request is None:
            raise ValueError(f"Reschedule request {uuid} not found")
        return request

    async def approve_request(self, uuid: UUID) -> RescheduleRequestDTO:
        request = await self.get_request(uuid)
        dt_start = datetime.combine(request.requested_date, request.requested_time)
        await self._repository.move_slot(
            request.slot_uuid,
            request.teacher_uuid,
            request.student_uuid,
            dt_start,
        )
        await self._repository.update_status(uuid, RescheduleStatus.APPROVED)
        return request

    async def reject_request(self, uuid: UUID) -> RescheduleRequestDTO:
        request = await self.get_request(uuid)
        await self._repository.update_status(uuid, RescheduleStatus.REJECTED)
        return request
