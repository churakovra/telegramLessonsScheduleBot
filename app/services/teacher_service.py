from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.teacher_repository import TeacherRepository
from app.schemas.user import UserDTO
from app.utils.enums.bot_values import UserRole
from app.utils.exceptions.teacher_exceptions import (
    TeacherAlreadyHasStudentException,
    TeacherStudentsNotFound,
)
from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class TeacherService:
    def __init__(
        self,
        session: AsyncSession | None = None,
        repository: TeacherRepository | None = None,
    ):
        if repository is None:
            if session is None:
                raise ValueError("TeacherService requires session or repository")
            repository = TeacherRepository(session)
        self._repository = repository

    async def get_teacher(self, username: str) -> UserDTO:
        teacher = await self._repository.get_teacher(username)
        if teacher is None:
            raise UserNotFoundException(username, UserRole.TEACHER)
        return teacher

    async def get_teacher_by_uuid(self, teacher_uuid: UUID) -> UserDTO:
        teacher = await self._repository.get_teacher(teacher_uuid)
        if teacher is None:
            raise UserNotFoundException(teacher_uuid, UserRole.TEACHER)
        return teacher

    async def get_all_teachers(self) -> list[UserDTO]:
        return await self._repository.get_all_teachers()

    async def _attach_student(
        self, teacher_uuid: UUID, student_uuid: UUID, uuid_lesson: UUID | None
    ):
        try:
            await self._repository.attach_student(
                teacher_uuid, student_uuid, uuid_lesson
            )
        except ValueError as e:
            logger.error(e)
            raise TeacherAlreadyHasStudentException(teacher_uuid, student_uuid)

    async def attach_students(
        self, *, teacher_uuid: UUID, students: list[UserDTO], uuid_lesson: UUID | None
    ):
        for student in students:
            await self._attach_student(teacher_uuid, student.uuid, uuid_lesson)

    async def _detach_student(self, teacher_uuid: UUID, student_uuid: UUID):
        await self._repository.detach_student(student_uuid, teacher_uuid)

    async def detach_student(self, teacher_uuid: UUID, student_uuid: UUID):
        """Detach a single student from a teacher."""
        await self._detach_student(teacher_uuid, student_uuid)

    async def detach_students(self, *, teacher_uuid: UUID, students: list[UserDTO]):
        for student in students:
            await self._detach_student(teacher_uuid, student.uuid)

    async def delete_students(self, students: list[UserDTO], teacher: UserDTO) -> None:
        for student in students:
            await self._repository.delete_students(student.uuid, teacher.uuid)

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
