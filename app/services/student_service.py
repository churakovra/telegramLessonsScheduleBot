from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.enums.bot_values import UserRoles
from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.repositories.student_repository import StudentRepository
from app.schemas.user_dto import UserDTO


class StudentService:
    def __init__(self, session: AsyncSession):
        self._repository = StudentRepository(session)

    async def get_student(self, username: str) -> UserDTO:
        student = await self._repository.get_student(username)
        if student is None:
            raise UserNotFoundException(username, UserRoles.STUDENT)
        return student
