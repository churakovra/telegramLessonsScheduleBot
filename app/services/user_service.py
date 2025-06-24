from uuid import UUID

from sqlalchemy.orm import Session

from app.enums.bot_values import UserRoles
from app.exceptions.user_exceptions import UserNotFoundException, UserChangeStatusException
from app.repositories.user_repository import UserRepository
from app.schemas.user_dto import UserDTO
from app.utils.bot_strings import bot_strings as bt
from app.utils.datetime_utils import day_format


class UserService:
    def __init__(self, session: Session):
        self._repository = UserRepository(session)

    def register_user(
            self,
            username: str,
            firstname: str,
            lastname: str | None,
            role: UserRoles,
            chat_id: int
    ) -> UUID:
        new_user = UserDTO.new_dto(
            username=username,
            firstname=firstname,
            lastname=lastname,
            role=role,
            chat_id=chat_id
        )
        self._repository.add_user(new_user)
        return new_user.uuid

    def add_role(self, initiator: str, username: str, role: UserRoles):
        initiator = self._repository.get_user(initiator)
        user = self._repository.get_user(username)
        if user or initiator is None:
            raise UserNotFoundException(username, role)

        i_student, i_teacher, i_admin = self.get_user_role(UserRoles.ADMIN)
        if not i_admin:
            raise UserChangeStatusException(user.username, UserRoles.ADMIN)
        self._repository.add_role(user.uuid, role)

    def get_user_info(self, username: str) -> str:
        user = self._repository.get_user(username)
        res = self.make_user_info_response(user)
        return res

    @staticmethod
    def make_user_info_response(user: UserDTO) -> str:
        try:
            result = (
                f"Пользователь {user.firstname} {user.lastname}\n"
                f"Имя пользователя {user.username}\n"
                f"Дата регистрации {user.dt_reg.strftime(day_format)}\n"
            )
        except Exception:
            result = bt.USER_INFO_ERROR

        return result

    @staticmethod
    def get_user_role(role: UserRoles) -> tuple[bool, bool, bool]:
        return (
            role == UserRoles.STUDENT,
            role == UserRoles.TEACHER,
            role == UserRoles.ADMIN,
        )
