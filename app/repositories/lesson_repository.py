from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.orm.lesson import Lesson
from app.db.orm.teacher_student import TeacherStudent
from app.schemas.lesson_dto import LessonDTO
from app.schemas.slot_dto import SlotDTO
from app.utils.logger import setup_logger


logger = setup_logger(__name__)


class LessonRepository:
    def __init__(self, session: AsyncSession):
        self._db = session

    async def create_lesson(
        self,
        uuid: UUID,
        label: str,
        duration: int,
        uuid_teacher: UUID,
        price: int,
    ) -> UUID:
        lesson = Lesson(
            uuid=uuid,
            label=label,
            duration=duration,
            uuid_teacher=uuid_teacher,
            price=price,
        )
        self._db.add(lesson)
        await self._db.commit()
        await self._db.refresh(lesson)
        return lesson.uuid

    async def get_students_lessons_by_slots(self, slots: list[SlotDTO]) -> dict[UUID, LessonDTO]:
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
