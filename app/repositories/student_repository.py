from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.orm.teacher_student import TeacherStudent
from app.database.orm.user import User
from app.schemas.student_dto import StudentDTO


class StudentRepository:
    def __init__(self, session: AsyncSession):
        self._db = session

    async def _get_student(self, username: str) -> User | None:
        stmt = select(User).where(
            and_(User.username == username, User.is_student == True)
        )
        student = await self._db.scalar(stmt)
        return student

    async def get_student_by_username(self, username: str) -> StudentDTO | None:
        student = await self._get_student(username)
        if student is None:
            return student
        return StudentDTO.model_validate(student)

    async def get_student_by_uuid(self, uuid: UUID):
        stmt = select(User).where(and_(User.uuid == uuid, User.is_student == True))
        return StudentDTO.model_validate(await self._db.scalar(stmt))

    async def get_students_by_teacher_uuid(
        self, teacher_uuid: UUID
    ) -> list[StudentDTO]:
        users = list()
        stmt = (
            select(User)
            .join(TeacherStudent, User.uuid == TeacherStudent.uuid_student)
            .where(TeacherStudent.uuid_teacher == teacher_uuid)
        )
        for user in await self._db.scalars(stmt):
            users.append(StudentDTO.model_validate(user))

        return users
