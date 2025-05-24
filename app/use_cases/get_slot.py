from uuid import UUID

from app.models.lesson_dto import LessonDTO
from app.repositories.slots_repo import SlotsRepo


async def get_slot_use_case(uuid_slot: UUID) -> LessonDTO:
    return await SlotsRepo.get_slot(uuid_slot)