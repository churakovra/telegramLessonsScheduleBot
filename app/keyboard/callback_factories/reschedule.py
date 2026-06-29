from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class StudentRescheduleCallback(CallbackData, prefix="st-resch"):
    slot_uuid: UUID


class StudentRescheduleConfirmCallback(CallbackData, prefix="st-resch-conf"):
    confirm: bool


class TeacherRescheduleListCallback(CallbackData, prefix="t-resch-list"):
    pass


class TeacherRescheduleDecisionCallback(CallbackData, prefix="t-resch-dec"):
    uuid: UUID
    approve: bool
