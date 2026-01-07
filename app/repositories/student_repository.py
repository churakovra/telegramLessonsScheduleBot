from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.orm.user import User
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
