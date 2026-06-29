from uuid import UUID

from sqlalchemy import and_, delete, func, not_, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.orm.slot import Slot
from app.database.orm.teacher_student import TeacherStudent
from app.database.orm.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import UserDTO
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class TeacherRepository(BaseRepository):
    def __init__(self, session: AsyncSession, *, auto_commit: bool = True):
        super().__init__(session, auto_commit=auto_commit)

    async def add_teacher(self, user_uuid: UUID) -> None:
        stmt = (
            update(User)
            .where(User.uuid == user_uuid)
            .values(is_student=False, is_teacher=True)
        )
        await self.execute(stmt)

    async def get_teacher(self, data: str | UUID) -> UserDTO | None:
        if isinstance(data, UUID):
            condition = User.uuid == data
        else:
            condition = User.username == data

        stmt = select(User).where(and_(condition, User.is_teacher.is_(True)))
        return await self.one_or_none_dto(stmt, UserDTO)

    async def get_all_teachers(self) -> list[UserDTO]:
        stmt = (
            select(User)
            .where(User.is_teacher.is_(True))
            .order_by(User.firstname.asc(), User.lastname.asc(), User.username.asc())
        )
        return await self.list_dto(stmt, UserDTO)

    async def update_profile(
        self,
        teacher_uuid: UUID,
        *,
        display_name: str | None,
        bio: str | None,
        subjects: str | None,
    ) -> None:
        stmt = (
            update(User)
            .where(and_(User.uuid == teacher_uuid, User.is_teacher.is_(True)))
            .values(display_name=display_name, bio=bio, subjects=subjects)
        )
        await self.execute(stmt)

    async def remove_teacher(self, teacher_uuid: UUID) -> None:
        stmt = (
            update(User)
            .where(User.uuid == teacher_uuid)
            .values(is_teacher=False, is_student=True)
        )
        await self.execute(stmt)

    async def attach_student(
        self, teacher_uuid: UUID, student_uuid: UUID, uuid_lesson: UUID | None
    ) -> TeacherStudent:
        try:
            teacher_student = TeacherStudent(
                uuid_teacher=teacher_uuid,
                uuid_student=student_uuid,
                uuid_lesson=uuid_lesson,
            )
            return await self.add(teacher_student)
        except IntegrityError as e:
            raise ValueError(str(e)) from e

    async def detach_student(self, student_uuid: UUID, teacher_uuid: UUID) -> None:
        stmt = delete(TeacherStudent).where(
            and_(
                TeacherStudent.uuid_teacher == teacher_uuid,
                TeacherStudent.uuid_student == student_uuid,
            )
        )
        logger.debug(f"delete stmt {stmt}, {teacher_uuid}, {student_uuid}")
        await self.execute(stmt)

    async def delete_students(self, student_uuid: UUID, teacher_uuid: UUID) -> None:
        await self.detach_student(student_uuid, teacher_uuid)

    async def get_students(self, teacher_uuid: UUID) -> list[UserDTO]:
        stmt = (
            select(User)
            .join(TeacherStudent, User.uuid == TeacherStudent.uuid_student)
            .where(TeacherStudent.uuid_teacher == teacher_uuid)
            .order_by(User.firstname.asc(), User.lastname.asc())
        )
        return await self.list_dto(stmt, UserDTO)

    async def get_unsigned_students(self, teacher_uuid: UUID) -> list[UserDTO]:
        ts_subquery = (
            select(TeacherStudent.uuid_student)
            .where(
                and_(
                    TeacherStudent.uuid_teacher == teacher_uuid,
                    TeacherStudent.uuid_lesson.is_not(None),
                )
            )
            .scalar_subquery()
        )
        slots_subquery = (
            select(Slot.uuid_student).where(Slot.dt_add > func.now()).scalar_subquery()
        )
        stmt = select(User).where(
            and_(User.uuid.in_(ts_subquery), not_(User.uuid.in_(slots_subquery)))
        )
        return await self.list_dto(stmt, UserDTO)
