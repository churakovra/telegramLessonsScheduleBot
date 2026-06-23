from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.orm.teacher_student import TeacherStudent
from app.database.orm.user import User
from app.repositories.base import BaseRepository
from app.schemas.student import StudentDTO


class StudentRepository(BaseRepository):
    def __init__(self, session: AsyncSession, *, auto_commit: bool = True):
        super().__init__(session, auto_commit=auto_commit)

    async def get_student_by_username(self, username: str) -> StudentDTO | None:
        stmt = select(User).where(
            and_(User.username == username, User.is_student.is_(True))
        )
        return await self.one_or_none_dto(stmt, StudentDTO)

    async def get_student(self, username: str) -> StudentDTO | None:
        return await self.get_student_by_username(username)

    async def get_student_by_uuid(self, uuid: UUID) -> StudentDTO | None:
        stmt = select(User).where(and_(User.uuid == uuid, User.is_student.is_(True)))
        return await self.one_or_none_dto(stmt, StudentDTO)

    async def get_students_by_teacher_uuid(
        self, teacher_uuid: UUID
    ) -> list[StudentDTO]:
        stmt = (
            select(User)
            .join(TeacherStudent, User.uuid == TeacherStudent.uuid_student)
            .where(TeacherStudent.uuid_teacher == teacher_uuid)
            .order_by(User.firstname.asc(), User.lastname.asc())
        )
        return await self.list_dto(stmt, StudentDTO)
