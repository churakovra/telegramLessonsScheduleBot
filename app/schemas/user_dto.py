from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from app.schemas.common import BaseDTO
from app.utils.enums.bot_values import UserRole


class CreateUserDTO(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    username: str
    firstname: str
    lastname: str | None = None
    role: UserRole
    is_student: bool = True
    is_teacher: bool = False
    is_admin: bool = False
    chat_id: int

    @model_validator(mode="after")
    def set_role_flags(self) -> "CreateUserDTO":
        self.is_student = self.role == UserRole.STUDENT
        self.is_teacher = self.role == UserRole.TEACHER
        self.is_admin = self.role == UserRole.ADMIN
        return self
    


class UserDTO(BaseDTO):
    uuid: UUID
    username: str
    firstname: str
    lastname: str | None
    is_student: bool
    is_teacher: bool
    is_admin: bool
    chat_id: int
    
    model_config = {"from_attributes": True}
    
    @property
    def role(self) -> UserRole:
        if self.is_admin:
            role = UserRole.ADMIN
        elif self.is_teacher:
            role = UserRole.TEACHER
        elif self.is_student:
            role = UserRole.STUDENT
        else:
            role = UserRole.NOT_DEFINED
        return role
