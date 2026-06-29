from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.schemas.common import BaseDTO


class CreateFeedbackDTO(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    slot_uuid: UUID
    student_uuid: UUID
    teacher_uuid: UUID
    rating: int
    comment: str | None = None


class FeedbackDTO(BaseDTO):
    uuid: UUID
    slot_uuid: UUID
    student_uuid: UUID
    teacher_uuid: UUID
    rating: int
    comment: str | None

    model_config = {"from_attributes": True}


class FeedbackPromptDTO(BaseModel):
    slot_uuid: UUID
    student_uuid: UUID
    teacher_uuid: UUID
    student_chat_id: int
    dt_start: datetime


class FeedbackInfoDTO(FeedbackDTO):
    student_name: str
    slot_time: datetime
