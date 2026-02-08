from datetime import UTC, datetime, timedelta, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator

from app.schemas.common import BaseDTO


class CreateSlotDTO(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    uuid_teacher: UUID
    dt_start: datetime
    dt_add: datetime = Field(default_factory=lambda: datetime.now(UTC))
    uuid_student: UUID | None
    dt_spot: datetime | None


class SlotDTO(BaseDTO):
    uuid: UUID
    uuid_teacher: UUID
    dt_start: datetime
    dt_add: datetime
    uuid_student: UUID | None
    dt_spot: datetime | None

    model_config = {"from_attributes": True}

    @field_validator("dt_start", "dt_add", "dt_spot", mode="before")
    @classmethod
    def convert_to_utc3(cls, value: datetime):
        utc3 = timezone(timedelta(hours=3))
        if value is None:
            return None
        if value.tzinfo is None:
            value = value.replace(tzinfo=utc3)
        return value.astimezone(utc3)
