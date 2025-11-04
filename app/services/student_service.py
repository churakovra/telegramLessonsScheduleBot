from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.student_repository import StudentRepository
from app.schemas.user_dto import UserDTO
from app.utils.enums.bot_values import UserRole
from app.utils.exceptions.user_exceptions import UserNotFoundException


class StudentService:
    def __init__(self, session: AsyncSession):
        self._repository = StudentRepository(session)

    async def get_student(self, username: str) -> UserDTO:
        student = await self._repository.get_student(username)
        if student is None:
            raise UserNotFoundException(username, UserRole.STUDENT)
        return student

    async def parse_students(self, students_raw: str) -> tuple[list[UserDTO], list[str]]:
        students = list[UserDTO]()
        unknown_students = list[str]()
        for username in students_raw.split(" "):
            try:
                students.append(await self.get_student(username.strip()))
            except UserNotFoundException:
                unknown_students.append(username.strip())
        return students, unknown_students
