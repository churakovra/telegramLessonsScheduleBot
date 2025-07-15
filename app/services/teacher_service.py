from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.bot_values import UserRoles
from app.exceptions.teacher_exceptions import TeacherStudentsNotFound
from app.exceptions.user_exceptions import UserNotFoundException
from app.repositories.teacher_repository import TeacherRepository
from app.schemas.user_dto import UserDTO


class TeacherService:
    def __init__(self, session: AsyncSession):
        self._repository = TeacherRepository(session)

    async def get_teacher(self, username: str) -> UserDTO:
        teacher = await self._repository.get_teacher(username)
        if teacher is None:
            raise UserNotFoundException(username, UserRoles.TEACHER)
        return teacher

    async def attach_student(self, *, teacher_uuid: UUID, student_uuid: UUID):
        await self._repository.attach_student(teacher_uuid, student_uuid)

    async def get_students(self, teacher_uuid: UUID) -> list[UserDTO]:
        students = await self._repository.get_students(teacher_uuid)
        if len(students) <= 0:
            raise TeacherStudentsNotFound(teacher_uuid)
        return students

    async def get_unsigned_students(self, teacher_uuid: UUID) -> list[UserDTO]:
        students = await self._repository.get_unsigned_students(teacher_uuid)
        if len(students) <= 0:
            raise TeacherStudentsNotFound(teacher_uuid)
        return students
