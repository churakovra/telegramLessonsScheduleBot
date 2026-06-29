from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.schemas.common import BaseDTO
from app.utils.enums.bot_values import JoinRequestStatus


class CreateJoinRequestDTO(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    student_uuid: UUID
    teacher_uuid: UUID
    status: JoinRequestStatus = JoinRequestStatus.PENDING


class JoinRequestDTO(BaseDTO):
    uuid: UUID
    student_uuid: UUID
    teacher_uuid: UUID
    status: JoinRequestStatus

    model_config = {"from_attributes": True}


class JoinRequestInfoDTO(JoinRequestDTO):
    student_username: str
    student_firstname: str
    student_lastname: str | None
    student_chat_id: int
