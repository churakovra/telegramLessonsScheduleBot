import asyncio

from app.utils.bot_values import BotValues as bv
from app.services.get_user_status_from_db import get_user_status

async def check_user_status(username: str, expected_status: bv.UserRoles):
    user_status = await get_user_status(username)
    return user_status == expected_status