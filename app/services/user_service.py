from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.schemas.user_dto import CreateUserDTO, UserDTO
from app.utils.bot_strings import BotStrings
from app.utils.datetime_utils import day_format
from app.utils.enums.bot_values import UserRole
from app.utils.exceptions.user_exceptions import (
    UserChangeRoleException,
    UserNotFoundException,
    UserUnknownRoleException,
)


class UserService:
    def __init__(self, session: AsyncSession):
        self._repository = UserRepository(session)

    async def register_user(
        self,
        username: str,
        firstname: str,
        lastname: str | None,
        role: UserRole,
        chat_id: int,
    ) -> UUID:
        new_user = CreateUserDTO(
            username=username,
            firstname=firstname,
            lastname=lastname,
            role=role,
            chat_id=chat_id
        )
        user = await self._repository.add_user(new_user)
        return user.uuid

    async def add_role(self, initiator_username: str, username: str, role: UserRole):
        initiator = await self._repository.get_user(initiator_username.strip())
        user = await self._repository.get_user(username.strip())
        if not initiator:
            raise UserNotFoundException(initiator_username, UserRole.ADMIN)
        elif not user:
            raise UserNotFoundException(username, role)
        if not initiator.is_admin:
            raise UserChangeRoleException(
                user.username, UserRole.ADMIN, initiator_username
            )
        try:
            await self._repository.edit_role(user.uuid, role, True)
        except ValueError:
            raise UserUnknownRoleException(role)

    async def get_user(self, username: str) -> UserDTO:
        user = await self._repository.get_user(username)
        if user is None:
            raise UserNotFoundException(username, None)
        return user

    async def get_user_info(self, username: str) -> str:
        user = await self.get_user(username)
        res = self.make_user_info_response(user)
        return res

    @staticmethod
    def make_user_info_response(user: UserDTO) -> str:
        try:
            result = (
                f"Пользователь {user.firstname} {user.lastname}\n"
                f"Имя пользователя {user.username}\n"
                f"Дата регистрации {user.created_at.strftime(day_format)}\n"
            )
        except Exception:
            result = BotStrings.User.USER_INFO_ERROR

        return result
    

    async def delete_user(self, user_uuid: UUID):
        await self._repository.delete_user(user_uuid)
