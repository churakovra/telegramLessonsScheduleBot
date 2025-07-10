from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel


class SlotDTO(BaseModel):
    uuid: UUID
    uuid_teacher: UUID
    dt_start: datetime
    dt_add: datetime
    uuid_student: UUID | None
    dt_spot: datetime | None

    @classmethod
    def new_dto(
            cls,
            uuid_teacher: UUID,
            dt_start: datetime,
            uuid_student: UUID | None,
            dt_spot: datetime | None
    ):
        return cls(
            uuid=uuid4(),
            uuid_teacher=uuid_teacher,
            dt_start=dt_start,
            dt_add=datetime.now(timezone.utc).astimezone(),
            uuid_student=uuid_student,
            dt_spot=dt_spot
        )
