from app.models.lesson_dto import LessonDTO
from app.services.slots_service import SlotsService


async def assign_slot_use_case(slot: LessonDTO, user: str):
    await SlotsService.assign_slot(slot, user)
