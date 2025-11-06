from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, field_validator


class SlotDTO(BaseModel):
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

    @classmethod
    def new_dto(
        cls,
        uuid_teacher: UUID,
        dt_start: datetime,
        uuid_student: UUID | None,
        dt_spot: datetime | None,
    ):
        utc3 = timezone(timedelta(hours=3))
        return cls(
            uuid=uuid4(),
            uuid_teacher=uuid_teacher,
            dt_start=dt_start,
            dt_add=datetime.now(utc3),
            uuid_student=uuid_student,
            dt_spot=dt_spot,
        )
