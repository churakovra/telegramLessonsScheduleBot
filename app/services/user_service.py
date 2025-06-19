from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.user_exceptions import ChangeUserStatusError, GetUserError
from app.models.user_dto import UserDTO
from app.repositories.user_repository import UserRepository
from app.utils.bot_strings import bot_strings as bt
from app.utils.bot_values import BotValues
from app.utils.datetime_utils import day_format

roles = BotValues.UserRoles


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

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
