from uuid import UUID

from app.keyboards.slots_for_students_markup import get_slots_for_students_markup
from app.repositories.slots_repo import SlotsRepo


async def get_slots_markup_use_case(uuid_day: UUID, chat_id: int):
    slots = await SlotsRepo.get_slots(uuid_day)
    return get_slots_for_students_markup(slots, chat_id)