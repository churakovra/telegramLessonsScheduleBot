from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.student_repository import StudentRepository
from app.schemas.lesson_dto import LessonDTO
from app.schemas.student_dto import StudentDTO
from app.utils.enums.bot_values import UserRole
from app.utils.exceptions.teacher_exceptions import TeacherStudentsNotFound
from app.utils.exceptions.user_exceptions import UserNotFoundException


class StudentService:
    def __init__(self, session: AsyncSession):
        self._repository = StudentRepository(session)

    async def get_student_by_username(self, username: str) -> StudentDTO:
        student = await self._repository.get_student_by_username(username)
        if student is None:
            raise UserNotFoundException(username, UserRole.STUDENT)
        return student

    async def get_student_by_uuid(self, uuid: UUID) -> StudentDTO:
        student = await self._repository.get_student_by_uuid(uuid=uuid)
        if student is None:
            raise UserNotFoundException(uuid, UserRole.STUDENT)
        return student

    async def get_students_by_teacher_uuid(
        self, teacher_uuid: UUID
    ) -> list[StudentDTO]:
        students = await self._repository.get_students_by_teacher_uuid(teacher_uuid)
        if len(students) <= 0:
            raise TeacherStudentsNotFound(teacher_uuid)
        return students

    async def parse_students(
        self, students_raw: str
    ) -> tuple[list[StudentDTO], list[str]]:
        students = list[StudentDTO]()
        unknown_students = list[str]()
        for username in students_raw.split(" "):
            try:
                students.append(await self.get_student_by_username(username.strip()))
            except UserNotFoundException:
                unknown_students.append(username.strip())
        return students, unknown_students

    async def get_student_info(
        self, student: StudentDTO, lessons: list[LessonDTO]
    ) -> str:
        name = " ".join([student.firstname, student.lastname or ""])
        username = student.username
        student_lessons = ", ".join([lesson.label for lesson in lessons])
        return f"Имя: {name}\nЛогин: {username}\nПредметы: {student_lessons}"
