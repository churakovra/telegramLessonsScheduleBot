from app.models.teacher_slot import Slot
from app.repositories.slots_repo import SlotsRepo


async def add_slots_use_case(slots: list[Slot]):
    await SlotsRepo.add_slots(slots)
