from app.services.get_user_from_db import get_user
from app.services.get_user_status_from_db import get_user_status
from app.utils.make_user_info_response import make_user_info_response


async def get_user_info(username: str) -> str:
    user = await get_user(username, session=None)
    user_status = await get_user_status(username)
    res = make_user_info_response(user, user_status)
    return res
