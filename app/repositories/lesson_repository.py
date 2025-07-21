from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.orm.lesson import Lesson


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
            price=price
        )
        self._db.add(lesson)
        await self._db.commit()
        await self._db.refresh(lesson)
        return lesson.uuid
