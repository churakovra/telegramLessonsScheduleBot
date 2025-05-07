from app.models.user import User
from app.models.user_dto import UserDTO

from app.utils.datetime_utils import day_format
from app.utils.bot_strings import bot_strings as bt
from app.utils.bot_values import BotValues as bv


def make_user_info_response(user: UserDTO, user_status: bv.UserRoles) -> str:
    try:
        result = (
            f"Пользователь {user.firstname} {user.lastname}\n"
            f"Имя пользователя {user.username}\n"
            f"Статус {user_status.value}\n"
            f"Дата регистрации {user.dt_reg.strftime(day_format)}\n"
        )
    except Exception:
        result = bt.USER_INFO_ERROR

    return result
