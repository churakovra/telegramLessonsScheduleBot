from app.exceptions.user_exceptions import UserStatusError, ChangeUserStatusError
from app.services.user_service import UserService
from app.use_cases.check_user_status import check_user_status_use_case

from app.utils.bot_values import BotValues

UserRoles = BotValues.UserRoles


async def make_teacher_use_case(initiator_username, new_teacher_username):
    try:
        await check_user_status_use_case(initiator_username, UserRoles.ADMIN)
        await check_user_status_use_case(new_teacher_username, UserRoles.STUDENT)
    except UserStatusError:
        return False

    try:
        await UserService.change_user_status(initiator_username, new_teacher_username, UserRoles.TEACHER)
    except ChangeUserStatusError:
        pass
