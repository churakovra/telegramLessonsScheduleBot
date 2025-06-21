from uuid import UUID


class SlotValidationException(Exception):
    def __init__(self):
        self.message = f"Error validating slot"


class SlotAssignError(Exception):
    def __init__(self, user_uuid: UUID, slot_uuid: UUID):
        self.message = f"Can't assign user {user_uuid} to slot {slot_uuid}"
