from app.services.user_service import UserService
from app.utils.bot_values import BotValues

roles = BotValues.UserRoles


class TeacherService(UserService):
    @staticmethod
    async def get_teachers_students():
        pass

    @staticmethod
    async def check_user_status(username: str, expected_status: roles = roles.TEACHER) -> bool:
        return await UserService.check_user_status(username, expected_status)
