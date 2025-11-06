import uuid
from uuid import UUID

from pydantic import BaseModel


class LessonDTO(BaseModel):
    uuid: UUID
    label: str
    duration: int
    uuid_teacher: UUID
    price: int
    
    model_config = {"from_attributes": True}

    @classmethod
    def new_dto(cls, label: str, duration: int, uuid_teacher: UUID, price: int):
        return cls(
            uuid=uuid.uuid4(),
            label=label,
            duration=duration,
            uuid_teacher=uuid_teacher,
            price=price
        )
