from uuid import UUID

from app.models.teacher_slot import Slot
from app.repositories.slots_repo import SlotsRepo


async def add_slots_use_case(slots: list[Slot]) -> dict[str, UUID]:
    return await SlotsRepo.add_slots(slots)
