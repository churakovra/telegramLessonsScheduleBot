from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.schemas.common import BaseDTO
from app.utils.enums.bot_values import NotificationTriggerType


class CreateNotificationDTO(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    teacher_uuid: UUID
    text: str
    trigger_type: NotificationTriggerType
    minutes_before: int
    is_active: bool = True


class NotificationDTO(BaseDTO):
    uuid: UUID
    teacher_uuid: UUID
    text: str
    trigger_type: NotificationTriggerType
    minutes_before: int
    is_active: bool

    model_config = {"from_attributes": True}
