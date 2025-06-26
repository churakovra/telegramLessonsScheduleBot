from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel

from app.enums.bot_values import UserRoles
from app.services.user_service import UserService


class UserDTO(BaseModel):
    uuid: UUID | None = None
    username: str
    firstname: str
    lastname: str
    is_student: bool
    is_teacher: bool
    is_admin: bool
    chat_id: int
    dt_reg: datetime
    dt_edit: datetime

    @classmethod
    def new_dto(
            cls,
            username: str,
            firstname: str,
            lastname: str | None,
            role: UserRoles,
            chat_id: int,
    ):
        is_student, is_teacher, is_admin = UserService.get_user_role(role)
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
