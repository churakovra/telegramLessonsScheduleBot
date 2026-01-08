from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.schemas.common import BaseDTO


class CreateLessonDTO(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    label: str
    duration: int
    uuid_teacher: UUID
    price: int


class LessonDTO(BaseDTO):
    uuid: UUID
    label: str
    duration: int
    uuid_teacher: UUID
    price: int
    
    model_config = {"from_attributes": True}

