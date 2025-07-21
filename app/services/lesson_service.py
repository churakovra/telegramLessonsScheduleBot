from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.lesson_repository import LessonRepository
from app.schemas.lesson_dto import LessonDTO


class LessonService:
    def __init__(self, session: AsyncSession):
        self._repository = LessonRepository(session)

    async def create_lesson(
            self,
            label,
            duration,
            uuid_teacher,
            price,
    ) -> UUID:
        lesson = LessonDTO.new_dto(
            label=label,
            duration=duration,
            uuid_teacher=uuid_teacher,
            price=price
        )

        await self._repository.create_lesson(**lesson.model_dump())
        return lesson.uuid
