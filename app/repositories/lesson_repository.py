from uuid import UUID

from sqlalchemy import and_, exists, not_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.orm.lesson import Lesson
from app.database.orm.teacher_student import TeacherStudent
from app.schemas.lesson_dto import CreateLessonDTO, LessonDTO
from app.schemas.slot_dto import SlotDTO
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class LessonRepository:
    def __init__(self, session: AsyncSession):
        self.database = session

    async def create_lesson(self, lesson_dto: CreateLessonDTO) -> Lesson:
        lesson = Lesson(**lesson_dto.model_dump())
        self.database.add(lesson)
        await self.database.commit()
        await self.database.refresh(lesson)
        return lesson

    async def get_students_lessons_by_slots(
        self, slots: list[SlotDTO]
    ) -> dict[UUID, LessonDTO]:
        stmt = (
            select(Lesson, TeacherStudent.uuid_student)
            .join(TeacherStudent, Lesson.uuid == TeacherStudent.uuid_lesson)
            .where(
                TeacherStudent.uuid_student.in_(
                    [slot.uuid_student for slot in slots if slot.uuid_student]
                ),
                TeacherStudent.uuid_teacher == slots[0].uuid_teacher,
            )
        )

        result = dict[UUID, LessonDTO]()
        for lesson, student_uuid in await self.database.execute(stmt):
            result[student_uuid] = lesson
        return result

    async def get_teacher_lessons(self, teacher_uuid: UUID) -> list[LessonDTO]:
        lessons = list()
        stmt = (
            select(Lesson)
            .where(Lesson.uuid_teacher == teacher_uuid)
            .order_by(Lesson.label.asc())
        )
        for lesson in await self.database.scalars(stmt):
            lessons.append(LessonDTO.model_validate(lesson))
        return lessons

    async def get_student_lessons(self, student_uuid: UUID) -> list[LessonDTO]:
        lessons = list()
        stmt = (
            select(Lesson)
            .join(TeacherStudent, Lesson.uuid == TeacherStudent.uuid_lesson)
            .where(TeacherStudent.uuid_student == student_uuid)
        )
        for lesson in await self.database.scalars(stmt):
            lessons.append(LessonDTO.model_validate(lesson))
        return lessons

    async def detach_lesson(self, lesson_uuid: UUID) -> None:
        stmt = (
            update(TeacherStudent)
            .where(TeacherStudent.uuid_lesson == lesson_uuid)
            .values(uuid_lesson=None)
        )
        await self.database.execute(stmt)
        await self.database.commit()

    async def delete_lesson(self, lesson_uuid: UUID) -> None:
        stmt = delete(Lesson).where(Lesson.uuid == lesson_uuid)
        await self.database.execute(stmt)
        await self.database.commit()

    async def update_lesson(self, lesson_uuid: UUID, values: dict) -> None:
        stmt = update(Lesson).where(Lesson.uuid == lesson_uuid).values(values)
        await self.database.execute(stmt)
        await self.database.commit()

    async def get_lesson_or_none(self, lesson_uuid: UUID) -> Lesson | None:
        stmt = select(Lesson).where(Lesson.uuid == lesson_uuid)
        lesson = await self.database.scalar(stmt)
        return lesson

    async def get_lessons_to_attach(
        self, teacher_uuid: UUID, student_uuid: UUID
    ) -> list[LessonDTO]:
        lessons = []
        stmt = (
            select(Lesson)
            .outerjoin(
                TeacherStudent,
                and_(
                    Lesson.uuid == TeacherStudent.uuid_lesson,
                    TeacherStudent.uuid_student == student_uuid,
                    TeacherStudent.uuid_teacher == teacher_uuid
                )
            )
            .where(TeacherStudent.uuid_lesson.is_(None))
        )
        logger.debug(stmt)
        for lesson in await self.database.scalars(stmt):
            logger.debug(lesson)
            lessons.append(LessonDTO.model_validate(lesson))
        return lessons


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
        await self.database.execute(stmt)
        await self.database.commit()
