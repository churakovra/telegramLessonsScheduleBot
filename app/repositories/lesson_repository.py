from uuid import UUID

from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.orm.lesson import Lesson
from app.database.orm.teacher_student import TeacherStudent
from app.repositories.base import BaseRepository
from app.schemas.lesson import CreateLessonDTO, LessonDTO
from app.schemas.slot import SlotDTO
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class LessonRepository(BaseRepository):
    def __init__(self, session: AsyncSession, *, auto_commit: bool = True):
        super().__init__(session, auto_commit=auto_commit)

    async def create_lesson(self, lesson_dto: CreateLessonDTO) -> LessonDTO:
        lesson = Lesson(**lesson_dto.model_dump())
        return LessonDTO.model_validate(await self.add(lesson))

    async def get_students_lessons_by_slots(
        self, slots: list[SlotDTO]
    ) -> dict[UUID, LessonDTO]:
        student_uuids = [slot.uuid_student for slot in slots if slot.uuid_student]
        if not slots or not student_uuids:
            return {}

        stmt = (
            select(Lesson, TeacherStudent.uuid_student)
            .join(TeacherStudent, Lesson.uuid == TeacherStudent.uuid_lesson)
            .where(
                TeacherStudent.uuid_student.in_(student_uuids),
                TeacherStudent.uuid_teacher == slots[0].uuid_teacher,
            )
        )

        result = dict[UUID, LessonDTO]()
        for lesson, student_uuid in await self.session.execute(stmt):
            result[student_uuid] = LessonDTO.model_validate(lesson)
        return result

    async def get_teacher_lessons(self, teacher_uuid: UUID) -> list[LessonDTO]:
        stmt = (
            select(Lesson)
            .where(Lesson.uuid_teacher == teacher_uuid)
            .order_by(Lesson.label.asc())
        )
        return await self.list_dto(stmt, LessonDTO)

    async def get_student_lessons(self, student_uuid: UUID) -> list[LessonDTO]:
        stmt = (
            select(Lesson)
            .join(TeacherStudent, Lesson.uuid == TeacherStudent.uuid_lesson)
            .where(TeacherStudent.uuid_student == student_uuid)
            .order_by(Lesson.label.asc())
        )
        return await self.list_dto(stmt, LessonDTO)

    async def detach_lesson(self, lesson_uuid: UUID) -> None:
        stmt = (
            update(TeacherStudent)
            .where(TeacherStudent.uuid_lesson == lesson_uuid)
            .values(uuid_lesson=None)
        )
        await self.execute(stmt)

    async def delete_lesson(self, lesson_uuid: UUID) -> None:
        stmt = delete(Lesson).where(Lesson.uuid == lesson_uuid)
        await self.execute(stmt)

    async def update_lesson(self, lesson_uuid: UUID, values: dict) -> None:
        if not values:
            return

        stmt = update(Lesson).where(Lesson.uuid == lesson_uuid).values(values)
        await self.execute(stmt)

    async def get_lesson_or_none(self, lesson_uuid: UUID) -> Lesson | None:
        stmt = select(Lesson).where(Lesson.uuid == lesson_uuid)
        return await self.scalar(stmt)

    async def get_lessons_to_attach(
        self, teacher_uuid: UUID, student_uuid: UUID
    ) -> list[LessonDTO]:
        stmt = (
            select(Lesson)
            .outerjoin(
                TeacherStudent,
                and_(
                    Lesson.uuid == TeacherStudent.uuid_lesson,
                    TeacherStudent.uuid_student == student_uuid,
                    TeacherStudent.uuid_teacher == teacher_uuid,
                ),
            )
            .where(
                Lesson.uuid_teacher == teacher_uuid,
                TeacherStudent.uuid_lesson.is_(None),
            )
            .order_by(Lesson.label.asc())
        )
        logger.debug(stmt)
        return await self.list_dto(stmt, LessonDTO)

    async def get_lessons_to_detach(
        self, teacher_uuid: UUID, student_uuid: UUID
    ) -> list[LessonDTO]:
        stmt = (
            select(Lesson)
            .join(TeacherStudent, Lesson.uuid == TeacherStudent.uuid_lesson)
            .where(
                TeacherStudent.uuid_student == student_uuid,
                TeacherStudent.uuid_teacher == teacher_uuid,
            )
            .order_by(Lesson.label.asc())
        )
        return await self.list_dto(stmt, LessonDTO)

    async def attach_lesson(
        self, student_uuid: UUID, teacher_uuid: UUID, lesson_uuid: UUID
    ) -> None:
        stmt = (
            update(TeacherStudent)
            .where(
                and_(
                    TeacherStudent.uuid_teacher == teacher_uuid,
                    TeacherStudent.uuid_student == student_uuid,
                )
            )
            .values({"uuid_lesson": lesson_uuid})
        )
        await self.execute(stmt)

    async def detach_specific_lesson(
        self, student_uuid: UUID, teacher_uuid: UUID, lesson_uuid: UUID
    ) -> None:
        stmt = (
            update(TeacherStudent)
            .where(
                and_(
                    TeacherStudent.uuid_teacher == teacher_uuid,
                    TeacherStudent.uuid_student == student_uuid,
                    TeacherStudent.uuid_lesson == lesson_uuid,
                )
            )
            .values({"uuid_lesson": None})
        )
        await self.execute(stmt)

    async def get_lesson_by_id(self, lesson_id: int) -> Lesson | None:
        stmt = select(Lesson).where(Lesson.id == lesson_id)
        return await self.scalar(stmt)
