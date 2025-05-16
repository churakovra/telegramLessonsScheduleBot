from app.exceptions.slot_exceptions import SlotValidationError
from app.models.teacher_slot import Slot
from app.services.slots_service import SlotsService


async def set_new_slots_use_case(slots_raw: str, message_from: str) -> list[Slot] | None:
    slots = await SlotsService.parse_slots(slots_raw, message_from)
    slots_valid = SlotsService.validate_slots(slots)
    if not slots_valid:
        raise SlotValidationError()
    return slots
