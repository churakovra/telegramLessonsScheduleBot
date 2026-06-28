from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import and_, delete, distinct, extract, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.database.orm.lesson import Lesson
from app.database.orm.slot import Slot
from app.database.orm.teacher_student import TeacherStudent
from app.database.orm.user import User
from app.repositories.base import BaseRepository
from app.schemas.slot import CreateSlotDTO, SlotDTO
from app.utils.exceptions.slot_exceptions import SlotAlreadyTakenException


class SlotRepository(BaseRepository):
    def __init__(self, session: AsyncSession, *, auto_commit: bool = True):
        super().__init__(session, auto_commit=auto_commit)

    async def add_slots(self, slots_dto: list[CreateSlotDTO]) -> None:
        slots = [Slot(**slot.model_dump()) for slot in slots_dto]
        await self.add_many(slots)

    async def find_slots_by_starts(
        self, teacher_uuid: UUID, dt_starts: list[datetime]
    ) -> list[SlotDTO]:
        if not dt_starts:
            return []

        stmt = (
            select(Slot)
            .where(Slot.uuid_teacher == teacher_uuid, Slot.dt_start.in_(dt_starts))
            .order_by(Slot.dt_start.asc())
        )
        return await self.list_dto(stmt, SlotDTO)

    async def get_slot(self, slot_uuid: UUID) -> SlotDTO | None:
        stmt = select(Slot).where(Slot.uuid == slot_uuid)
        return await self.one_or_none_dto(stmt, SlotDTO)

    async def get_slots(
        self, teacher_uuid: UUID, week: int | None = None
    ) -> list[SlotDTO]:
        conditions = [Slot.uuid_teacher == teacher_uuid]
        if week is not None:
            conditions.append(extract("week", Slot.dt_start) == week)

        stmt = select(Slot).where(and_(*conditions)).order_by(Slot.dt_start.asc())
        return await self.list_dto(stmt, SlotDTO)

    async def get_free_slots(self, teacher_uuid: UUID) -> list[SlotDTO]:
        stmt = (
            select(Slot)
            .where(
                and_(
                    Slot.uuid_teacher == teacher_uuid,
                    Slot.dt_start > func.now(),
                    Slot.uuid_student.is_(None),
                )
            )
            .order_by(Slot.dt_start.asc())
        )
        return await self.list_dto(stmt, SlotDTO)

    async def get_day_free_slots(
        self, day: datetime, teacher_uuid: UUID
    ) -> list[SlotDTO]:
        stmt = (
            select(Slot)
            .where(
                and_(
                    func.date(Slot.dt_start) == day.date(),
                    Slot.uuid_teacher == teacher_uuid,
                    Slot.uuid_student.is_(None),
                )
            )
            .order_by(Slot.dt_start.asc())
        )
        return await self.list_dto(stmt, SlotDTO)

    async def get_student_booked_slots(
        self, student_uuid: UUID, start_at: datetime, end_at: datetime
    ) -> list[SlotDTO]:
        stmt = (
            select(Slot)
            .where(
                Slot.uuid_student == student_uuid,
                Slot.dt_start >= start_at,
                Slot.dt_start < end_at,
            )
            .order_by(Slot.dt_start.asc())
        )
        return await self.list_dto(stmt, SlotDTO)

    async def unassign_slot(self, student_uuid: UUID, slot_uuid: UUID) -> SlotDTO | None:
        slot = await self.get_slot(slot_uuid)
        if slot is None or slot.uuid_student != student_uuid:
            return None

        stmt = (
            update(Slot)
            .where(Slot.uuid == slot_uuid, Slot.uuid_student == student_uuid)
            .values(uuid_student=None, dt_spot=None)
        )
        await self.execute(stmt)
        return slot

    async def get_booked_slots_for_stats(
        self,
        user_uuid: UUID,
        start_at: datetime,
        end_at: datetime,
        *,
        as_teacher: bool,
    ) -> list[tuple[Slot, User, User, Lesson | None]]:
        teacher = aliased(User)
        student = aliased(User)
        conditions = [
            Slot.uuid_student.is_not(None),
            Slot.dt_start >= start_at,
            Slot.dt_start < end_at,
        ]
        if as_teacher:
            conditions.append(Slot.uuid_teacher == user_uuid)
        else:
            conditions.append(Slot.uuid_student == user_uuid)

        stmt = (
            select(
                Slot,
                teacher,
                student,
                Lesson,
            )
            .join(teacher, Slot.uuid_teacher == teacher.uuid)
            .join(student, Slot.uuid_student == student.uuid)
            .outerjoin(
                TeacherStudent,
                and_(
                    TeacherStudent.uuid_teacher == Slot.uuid_teacher,
                    TeacherStudent.uuid_student == Slot.uuid_student,
                ),
            )
            .outerjoin(Lesson, Lesson.uuid == TeacherStudent.uuid_lesson)
            .where(and_(*conditions))
            .order_by(Slot.dt_start.asc())
        )
        return list(await self.session.execute(stmt))

    async def get_admin_week_stats(
        self, start_at: datetime, end_at: datetime
    ) -> tuple[int, int]:
        stmt = select(
            func.count(Slot.uuid),
            func.count(distinct(Slot.uuid_teacher)),
        ).where(
            Slot.uuid_student.is_not(None),
            Slot.dt_start >= start_at,
            Slot.dt_start < end_at,
        )
        total_lessons, active_teachers = (await self.session.execute(stmt)).one()
        return int(total_lessons), int(active_teachers)

    async def assign_slot(self, student_uuid: UUID, slot_uuid: UUID) -> None:
        stmt = (
            update(Slot)
            .where(
                Slot.uuid == slot_uuid,
                Slot.uuid_student.is_(None),
                Slot.dt_start > func.now(),
            )
            .values(uuid_student=student_uuid, dt_spot=datetime.now(UTC).astimezone())
        )
        result = await self.session.execute(stmt)
        await self.session.flush()
        if result.rowcount == 0:
            if self.auto_commit:
                await self.session.rollback()
            raise SlotAlreadyTakenException(slot_uuid)
        if self.auto_commit:
            await self.session.commit()

    async def delete_slots(self, slots: list[SlotDTO]) -> None:
        if not slots:
            return

        stmt = delete(Slot).where(Slot.uuid.in_([slot.uuid for slot in slots]))
        await self.execute(stmt)

    async def delete_slots_attached_to_student(self, student_uuid: UUID) -> None:
        stmt = delete(Slot).where(Slot.uuid_student == student_uuid)
        await self.execute(stmt)

    async def delete_slot(self, slot_uuid: UUID) -> None:
        stmt = delete(Slot).where(Slot.uuid == slot_uuid)
        await self.execute(stmt)
