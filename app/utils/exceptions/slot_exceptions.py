from uuid import UUID


class SlotValidationException(Exception):
    def __init__(self):
        self.message = f"Error validating slot"


class SlotAssignException(Exception):
    def __init__(self, user_uuid: UUID, slot_uuid: UUID):
        self.user_uuid = user_uuid
        self.slot_uuid = slot_uuid
        self.message = f"Can't assign user {user_uuid} to slot {slot_uuid}"


class SlotNotFoundException(Exception):
    def __init__(self, slot_uuid: UUID):
        self.slot_uuid = slot_uuid
        self.message = f"Slot {slot_uuid} were not found"


class SlotFreeNotFoundException(Exception):
    def __init__(self, teacher_uuid: UUID):
        self.teacher_uuid = teacher_uuid
        self.message = f"Free slots for teacher {teacher_uuid} were not found"
