from uuid import UUID

from sqlalchemy.orm import Session

from app.enums.bot_values import UserRoles
from app.exceptions.user_exceptions import ChangeUserStatusError, GetUserError
from app.repositories.user_repository import UserRepository
from app.schemas.user_dto import UserDTO
from app.utils.bot_strings import bot_strings as bt
from app.utils.datetime_utils import day_format


class UserService:
    def __init__(self, session: Session):
        self.repository = UserRepository(session)

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
        self.repository.add_user(new_user)
        return new_user.uuid

    async def get_user_info(self, username: str) -> str:
        user = await self.repository.get_user(username)
        user_status = await self.repository.get_user_roles(username)
        res = self.make_user_info_response(user, user_status)
        return res

    def make_user_info_response(self, user: UserDTO, user_status: list[roles]) -> str:
        try:
            result = (
                f"Пользователь {user.firstname} {user.lastname}\n"
                f"Имя пользователя {user.username}\n"
                f"Статус {user_status}\n"
                f"Дата регистрации {user.dt_reg.strftime(day_format)}\n"
            )
        except Exception:
            result = bt.USER_INFO_ERROR

        return result

    async def check_user_status(self, username: str, expected_status: roles) -> bool:
        user_status = self.repository.get_user_roles(username)
        return expected_status in user_status

    async def change_user_status(self, initiator_user: str, teacher_username: str, new_status: roles):
        if not await self.repository.change_user_status_in_db(initiator_user, teacher_username, new_status):
            raise ChangeUserStatusError
        return True

    async def check_user_exists(self, username: str) -> bool:
        try:
            await self.repository.get_user(username)
            return True
        except GetUserError:
            return False

    @staticmethod
    def get_user_role(role: UserRoles) -> tuple[bool, bool, bool]:
        return (
            role == UserRoles.STUDENT,
            role == UserRoles.TEACHER,
            role == UserRoles.ADMIN,
        )
