from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class StudentScheduleCallback(CallbackData, prefix="student-schedule"):
    pass


class StudentWeeklyScheduleCallback(CallbackData, prefix="student-weekly-schedule"):
    pass


class StudentSlotCancelCallback(CallbackData, prefix="cancel-st-slot"):
    uuid_slot: UUID
