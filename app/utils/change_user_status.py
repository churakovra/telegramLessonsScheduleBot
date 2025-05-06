from app.services.change_user_status_in_db import change_user_status_in_db
from app.utils.bot_values import BotValues as bv


async def change_user_status(initiator_user: str, teacher_username: str, new_status: bv.UserRoles):
    return await change_user_status_in_db(initiator_user, teacher_username, new_status)
