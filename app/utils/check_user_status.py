from app.services.get_user_status_from_db import get_user_status
from app.utils.bot_values import BotValues

roles = BotValues.UserRoles


async def check_user_status(username: str, expected_status: roles):
    user_status = await get_user_status(username)
    return expected_status in user_status
