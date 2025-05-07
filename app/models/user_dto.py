from dataclasses import dataclass
from datetime import datetime

from app.models.user import User


@dataclass
class UserDTO:
    id: int
    username: str
    firstname: str
    lastname: str | None
    dt_reg: datetime
    status: str | None = None

    @staticmethod
    def get_user_dto(user: User):
        result_user = UserDTO(
            id=user.id,
            username=user.username,
            firstname=user.firstname,
            lastname=user.lastname,
            dt_reg=user.dt_reg
        )
        return result_user