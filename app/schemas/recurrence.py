from datetime import date, time
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.schemas.common import BaseDTO


class CreateRecurrenceRuleDTO(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    teacher_uuid: UUID
    day_of_week: int
    time_start: time
    time_end: time
    slot_duration_minutes: int
    date_start: date
    date_end: date
    is_active: bool = True


class RecurrenceRuleDTO(BaseDTO):
    uuid: UUID
    teacher_uuid: UUID
    day_of_week: int
    time_start: time
    time_end: time
    slot_duration_minutes: int
    date_start: date
    date_end: date
    is_active: bool

    model_config = {"from_attributes": True}
