from dataclasses import dataclass
from datetime import datetime

from app.models.orm.user import User


@dataclass
class UserDTO:
    username: str
    firstname: str
    chat_id: int
    id: int | None = None
    lastname: str | None = None
    dt_reg: datetime | None = None
    status: str | None = None

    @staticmethod
    def get_user_dto(user: User):
        result_user = UserDTO(
            id=user.id,
            username=user.username,
            firstname=user.firstname,
            lastname=user.lastname,
            chat_id=user.chat_id,
            dt_reg=user.dt_reg
        )
        return result_user

    @staticmethod
    def register_user(username: str, firstname: str, chat_id: int, lastname: str | None = None):
        return UserDTO(
            username=username,
            firstname=firstname,
            chat_id=chat_id,
            lastname=lastname if lastname is not None else None
        )
