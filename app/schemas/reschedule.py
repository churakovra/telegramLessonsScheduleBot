from datetime import date, time
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.schemas.common import BaseDTO
from app.utils.enums.bot_values import RescheduleStatus


class CreateRescheduleRequestDTO(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    slot_uuid: UUID
    student_uuid: UUID
    teacher_uuid: UUID
    requested_date: date
    requested_time: time
    status: RescheduleStatus = RescheduleStatus.PENDING


class RescheduleRequestDTO(BaseDTO):
    uuid: UUID
    slot_uuid: UUID
    student_uuid: UUID
    teacher_uuid: UUID
    requested_date: date
    requested_time: time
    status: RescheduleStatus

    model_config = {"from_attributes": True}


class RescheduleRequestInfoDTO(RescheduleRequestDTO):
    student_name: str
    student_chat_id: int
    original_dt_start: str
