from uuid import UUID

from aiogram.types import InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.schemas.user_dto import UserDTO
from app.utils.bot_strings import BotStrings
from app.utils.datetime_utils import day_format
from app.utils.enums.bot_values import UserRoles
from app.utils.exceptions.user_exceptions import (
    UserChangeRoleException,
    UserNotFoundException,
    UserUnknownRoleException,
)
from app.utils.keyboards.main_menu_markup import get_main_menu_markup


class UserService:
    def __init__(self, session: AsyncSession):
        self._repository = UserRepository(session)

    async def register_user(
        self,
        username: str,
        firstname: str,
        lastname: str | None,
        role: UserRoles,
        chat_id: int,
    ) -> UUID:
        new_user = UserDTO.new_dto(
            username=username,
            firstname=firstname,
            lastname=lastname,
            role=role,
            chat_id=chat_id,
        )
        await self._repository.add_user(new_user)
        return new_user.uuid

    async def add_role(self, initiator_username: str, username: str, role: UserRoles):
        initiator = await self._repository.get_user(initiator_username.strip())
        user = await self._repository.get_user(username.strip())
        if not initiator:
            raise UserNotFoundException(initiator_username, UserRoles.ADMIN)
        elif not user:
            raise UserNotFoundException(username, role)

        if not initiator.is_admin:
            raise UserChangeRoleException(
                user.username, UserRoles.ADMIN, initiator_username
            )

        try:
            await self._repository.edit_role(user.uuid, role, True)
        except ValueError:
            raise UserUnknownRoleException(username, role)

    async def get_user(self, username: str) -> UserDTO:
        user = await self._repository.get_user(username)
        if user is None:
            raise UserNotFoundException(username, None)
        return user

    async def get_user_info(self, username: str) -> str:
        user = await self.get_user(username)
        res = self.make_user_info_response(user)
        return res

    async def get_user_menu(
        self, username: str
    ) -> tuple[UserDTO, InlineKeyboardMarkup]:
        user = await self.get_user(username)
        markup = get_main_menu_markup(user)
        return user, markup

    @staticmethod
    def make_user_info_response(user: UserDTO) -> str:
        try:
            result = (
                f"Пользователь {user.firstname} {user.lastname}\n"
                f"Имя пользователя {user.username}\n"
                f"Дата регистрации {user.dt_reg.strftime(day_format)}\n"
            )
        except Exception:
            result = BotStrings.USER_INFO_ERROR

        return result

    @staticmethod
    def get_user_role(role: UserRoles) -> tuple[bool, bool, bool]:
        return (
            role == UserRoles.STUDENT,
            role == UserRoles.TEACHER,
            role == UserRoles.ADMIN,
        )
