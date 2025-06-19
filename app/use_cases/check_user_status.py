from app.exceptions.user_exceptions import UserStatusError
from app.services.user_service import UserService
from app.use_cases.base import BaseUseCase
from app.utils.bot_values import BotValues

UserRoles = BotValues.UserRoles


class CheckUserStatusUseCase(BaseUseCase):

    async def check_user_status(self, username: str, role: UserRoles):
        user_service = UserService(self.session)
        if not await user_service.check_user_status(username, role):
            raise UserStatusError
