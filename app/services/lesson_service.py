from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.lesson_repository import LessonRepository
from app.schemas.lesson_dto import CreateLessonDTO, LessonDTO, UpdateLessonDTO
from app.schemas.slot_dto import SlotDTO
from app.utils.exceptions.lesson_exceptions import LessonsNotFoundException
from app.utils.logger import setup_logger
from app.schemas.student_dto import StudentDTO


logger = setup_logger(__name__)


class LessonService:
    def __init__(self, session: AsyncSession):
        self._repository = LessonRepository(session)

    async def create_lesson(
        self,
        label: str,
        duration: int,
        uuid_teacher: UUID,
        price: int,
    ) -> LessonDTO:
        new_lesson = CreateLessonDTO(
            label=label, duration=duration, uuid_teacher=uuid_teacher, price=price
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

    async def detach_lesson(self, lesson_uuid: UUID) -> None:
        await self._repository.detach_lesson(lesson_uuid)

    async def delete_lesson(self, lesson_uuid: UUID) -> None:
        await self._repository.delete_lesson(lesson_uuid)

    async def update_lesson(self, lesson_uuid: UUID, **kwargs) -> None:
        update = UpdateLessonDTO.model_validate(kwargs)
        update_dict = {
            k: v
            for k, v in update.model_dump(exclude_unset=True, exclude_none=True).items()
        }
        await self._repository.update_lesson(lesson_uuid, update_dict)

    async def get_lesson(self, lesson_uuid: UUID) -> LessonDTO:
        lesson = await self._repository.get_lesson_or_none(lesson_uuid)
        if not lesson:
            raise LessonsNotFoundException()
        return LessonDTO.model_validate(lesson)

    async def get_student_lessons(self, student_uuid: UUID) -> list[LessonDTO]:
        lessons = await self._repository.get_student_lessons(student_uuid)
        return lessons

    async def get_lesson_info(self, lesson: LessonDTO) -> str:
        label = f"*{lesson.label}*"
        duration = f"Длительность {lesson.duration} мин"
        price = f"Стоимость {lesson.price} руб"
        return f"{label}\n{duration}\n{price}"
    

    async def get_lessons_to_attach(self, student_uuid: UUID, teacher_uuid: UUID) -> list[LessonDTO]:
        lessons = await self._repository.get_lessons_to_attach(student_uuid, teacher_uuid)
        return lessons


    async def attach_lesson(self, student_uuid: UUID, teacher_uuid: UUID, lesson_uuid: UUID) -> None:
        await self._repository.attach_lesson(student_uuid, teacher_uuid, lesson_uuid)

    async def get_lessons_to_detach(self, student: StudentDTO): ...