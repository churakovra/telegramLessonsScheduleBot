from uuid import UUID

from sqlalchemy import and_, delete, func, not_, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.orm.slot import Slot
from app.database.orm.teacher_student import TeacherStudent
from app.database.orm.user import User
from app.schemas.user_dto import UserDTO
from app.utils.logger import setup_logger


logger = setup_logger(__name__)


class TeacherRepository:
    def __init__(self, session: AsyncSession):
        self._db = session

    async def add_teacher(self, user_uuid: UUID):
        stmt = (
            update(User)
            .where(User.uuid == user_uuid)
            .values(is_student=False)
            .values(is_teacher=True)
        )
        await self._db.execute(stmt)
        await self._db.commit()

    async def _get_teacher(self, data: str | UUID) -> User | None:
        if isinstance(data, UUID):
            condition = User.uuid == data
        else:
            condition = User.username == data

        stmt = select(User).where(and_(condition, User.is_teacher == True))
        teacher = await self._db.scalar(stmt)
        return teacher

    async def get_teacher(self, data: str | UUID) -> UserDTO | None:
        teacher = await self._get_teacher(data)
        if teacher is None:
            return teacher
        return UserDTO.model_validate(teacher)

    async def remove_teacher(self, teacher_uuid: UUID):
        stmt = (
            update(User)
            .where(User.uuid == teacher_uuid)
            .values(is_teacher=False)
            .values(is_student=True)
        )
        await self._db.execute(stmt)
        await self._db.commit()

    async def attach_student(
        self, teacher_uuid: UUID, student_uuid: UUID, uuid_lesson: UUID | None
    ) -> TeacherStudent:
        try:
            teacher_student = TeacherStudent(
                uuid_teacher=teacher_uuid,
                uuid_student=student_uuid,
                uuid_lesson=uuid_lesson,
            )
            self._db.add(teacher_student)
            await self._db.commit()
            await self._db.refresh(teacher_student)
            return teacher_student
        except IntegrityError as e:
            raise ValueError(str(e)) from e

    async def detach_student(self, student_uuid: UUID, teacher_uuid: UUID):
        stmt = delete(TeacherStudent).where(
            and_(
                TeacherStudent.uuid_teacher == teacher_uuid,
                TeacherStudent.uuid_student == student_uuid,
            )
        )
        logger.debug(f"delete stmt {stmt}, {teacher_uuid}, {student_uuid}")
        await self._db.execute(stmt)
        await self._db.commit()

    async def get_unsigned_students(self, teacher_uuid: UUID) -> list[UserDTO]:
        users = list()
        ts_subquery = (
            select(TeacherStudent.uuid_student)
            .where(
                and_(
                    TeacherStudent.uuid_teacher == teacher_uuid,
                    TeacherStudent.lesson != None,
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
        for user in await self._db.scalars(stmt):
            users.append(UserDTO.model_validate(user))
        return users
