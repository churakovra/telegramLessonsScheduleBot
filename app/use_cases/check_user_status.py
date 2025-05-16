from app.exceptions.user_exceptions import UserStatusError
from app.services.user_service import UserService
from app.utils.bot_values import BotValues

UserRoles = BotValues.UserRoles


async def check_user_status_use_case(username: str, role: UserRoles):
    if not await UserService.check_user_status(username, role):
        raise UserStatusError
