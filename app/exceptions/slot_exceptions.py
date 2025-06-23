from uuid import UUID


class SlotValidationException(Exception):
    def __init__(self):
        self.message = f"Error validating slot"


class SlotAssignException(Exception):
    def __init__(self, user_uuid: UUID, slot_uuid: UUID):
        self.message = f"Can't assign user {user_uuid} to slot {slot_uuid}"


class SlotFreeNotFoundException(Exception):
    def __init__(self, teacher_uuid: UUID):
        self.message = f"Free slots for teacher {teacher_uuid} were not found"
