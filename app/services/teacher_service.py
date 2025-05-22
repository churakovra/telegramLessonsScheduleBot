from app.models.user_dto import UserDTO
from app.repositories.teacher_repo import TeacherRepo
from app.services.user_service import UserService
from app.utils.bot_values import BotValues

roles = BotValues.UserRoles


class TeacherService(UserService):
    @staticmethod
    async def get_students(teacher_username: str) -> list[UserDTO]:
        return await TeacherRepo.get_students(teacher_username)

    @staticmethod
    async def check_user_status(username: str, expected_status: roles = roles.TEACHER) -> bool:
        return await UserService.check_user_status(username, expected_status)
