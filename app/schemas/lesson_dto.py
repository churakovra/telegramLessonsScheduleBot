from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.schemas.common import BaseDTO


class CreateLessonDTO(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    label: str
    duration: int
    uuid_teacher: UUID
    price: int


class UpdateLessonDTO(BaseModel):
    label: str | None = Field(default=None, alias="label")
    duration: int | None = Field(default=None, alias="duration")
    price: int | None = Field(default=None, alias="price")

    model_config = {"from_attributes": True}


class LessonDTO(BaseDTO):
    uuid: UUID
    label: str
    duration: int
    uuid_teacher: UUID
    price: int
    
    model_config = {"from_attributes": True}

