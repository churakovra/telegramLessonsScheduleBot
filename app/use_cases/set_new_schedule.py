from app.exceptions.slot_exceptions import SlotValidationError
from app.models.orm.teacher_slot import Slot
from app.services.slot_service import SlotService


async def set_new_schedule_use_case(slots_raw: str, message_from: str) -> list[Slot] | None:
    slots = await SlotService.parse_slots(slots_raw, message_from)
    slots_valid = SlotService.validate_slots(slots)
    if not slots_valid:
        raise SlotValidationError()
    return slots
