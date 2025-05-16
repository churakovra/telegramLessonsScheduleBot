from app.exceptions.user_exceptions import ChangeUserStatusError
from app.models.user_dto import UserDTO
from app.repositories.user_repo import UserRepo
from app.utils.bot_strings import bot_strings as bt
from app.utils.bot_values import BotValues
from app.utils.datetime_utils import day_format

roles = BotValues.UserRoles


class UserService:
    @staticmethod
    async def get_user_info(username: str) -> str:
        user = await UserRepo.get_user(username, session=None)
        user_status = await UserRepo.get_user_status(username)
        res = UserService.make_user_info_response(user, user_status)
        return res

    @staticmethod
    def make_user_info_response(user: UserDTO, user_status: list[roles]) -> str:
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

    @staticmethod
    async def check_user_status(username: str, expected_status: roles) -> bool:
        user_status = await UserRepo.get_user_status(username)
        return expected_status in user_status

    @staticmethod
    async def change_user_status(initiator_user: str, teacher_username: str, new_status: roles):
        if not await UserRepo.change_user_status_in_db(initiator_user, teacher_username, new_status):
            raise ChangeUserStatusError
