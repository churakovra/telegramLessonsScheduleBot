from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel

from app.utils.enums.bot_values import UserRole


class UserDTO(BaseModel):
    uuid: UUID
    username: str
    firstname: str
    lastname: str | None
    is_student: bool
    is_teacher: bool
    is_admin: bool
    chat_id: int
    dt_reg: datetime
    dt_edit: datetime
    
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

    @classmethod
    def new_dto(
            cls,
            username: str,
            firstname: str,
            lastname: str | None,
            role: UserRole,
            chat_id: int,
    ):
        is_student, is_teacher, is_admin = (
            role == UserRole.STUDENT,
            role == UserRole.TEACHER,
            role == UserRole.ADMIN,
        )
        return cls(
            uuid=uuid4(),
            username=username,
            firstname=firstname,
            lastname=lastname,
            is_student=is_student,
            is_teacher=is_teacher,
            is_admin=is_admin,
            chat_id=chat_id,
            dt_reg=datetime.now(timezone.utc).astimezone(),
            dt_edit=datetime.now(timezone.utc).astimezone()
        )
