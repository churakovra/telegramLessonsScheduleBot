from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.lesson_repository import LessonRepository
from app.schemas.lesson_dto import CreateLessonDTO, LessonDTO
from app.schemas.slot_dto import SlotDTO
from app.utils.exceptions.lesson_exceptions import LessonsNotFoundException
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class LessonService:
    def __init__(self, session: AsyncSession):
        self._repository = LessonRepository(session)

    async def create_lesson(
        self,
        label,
        duration,
        uuid_teacher,
        price,
    ) -> LessonDTO:
        new_lesson = CreateLessonDTO(
            label=label, 
            duration=duration, 
            uuid_teacher=uuid_teacher, 
            price=price
        )

        lesson = await self._repository.create_lesson(new_lesson)
        return LessonDTO.model_validate(lesson)

    async def get_students_lessons_by_slots(self, slots: list[SlotDTO]):
        lessons = await self._repository.get_students_lessons_by_slots(slots)
        if len(lessons.keys()) <= 0:
            raise LessonsNotFoundException()
        return lessons

    async def get_teacher_lessons(self, teacher_uuid: UUID) -> list[LessonDTO]:
        lessons = await self._repository.get_teacher_lessons(teacher_uuid)
        if len(lessons) <= 0:
            raise LessonsNotFoundException()
        return lessons


    async def detach_lesson(self, lesson_uuid: UUID):
        await self._repository.detach_lesson(lesson_uuid)


    async def delete_lesson(self, lesson_uuid: UUID) -> None:
        await self._repository.delete_lesson(lesson_uuid)