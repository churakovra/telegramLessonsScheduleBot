from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.orm.lesson import Lesson
from app.db.orm.teacher_student import TeacherStudent
from app.schemas.lesson_dto import CreateLessonDTO, LessonDTO
from app.schemas.slot_dto import SlotDTO
from app.utils.logger import setup_logger


logger = setup_logger(__name__)


class LessonRepository:
    def __init__(self, session: AsyncSession):
        self._db = session

    async def create_lesson(self, lesson_dto: CreateLessonDTO) -> Lesson:
        lesson = Lesson(**lesson_dto.model_dump())
        self._db.add(lesson)
        await self._db.commit()
        await self._db.refresh(lesson)
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
        for lesson, student_uuid in await self._db.execute(stmt):
            result[student_uuid] = lesson
        return result

    async def get_teacher_lessons(self, teacher_uuid: UUID) -> list[LessonDTO]:
        lessons = list()
        stmt = (
            select(Lesson)
            .where(Lesson.uuid_teacher == teacher_uuid)
            .order_by(Lesson.label.asc())
        )
        for lesson in await self._db.scalars(stmt):
            logger.debug(f"lesson {lesson}")
            lessons.append(LessonDTO.model_validate(lesson))
        return lessons

    async def detach_lesson(self, lesson_uuid: UUID) -> None:
        stmt = (
            update(TeacherStudent)
            .where(TeacherStudent.uuid_lesson == lesson_uuid)
            .values(uuid_lesson=None)
        )
        await self._db.execute(stmt)
        await self._db.commit()

    async def delete_lesson(self, lesson_uuid: UUID) -> None:
        stmt = delete(Lesson).where(Lesson.uuid == lesson_uuid)
        await self._db.execute(stmt)
        await self._db.commit()


    async def update_lesson(self, lesson_uuid: UUID, values: dict) -> None:
        stmt = update(Lesson).where(Lesson.uuid == lesson_uuid).values(values)
        await self._db.execute(stmt)
        await self._db.commit()