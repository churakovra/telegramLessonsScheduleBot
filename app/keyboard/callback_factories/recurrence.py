from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class RecurrenceCreateCallback(CallbackData, prefix="rec-create"):
    pass


class RecurrenceListCallback(CallbackData, prefix="rec-list"):
    pass


class RecurrenceDeleteCallback(CallbackData, prefix="rec-delete"):
    uuid: UUID


class RecurrenceDayCallback(CallbackData, prefix="rec-day"):
    day_of_week: int


class RecurrenceConfirmCallback(CallbackData, prefix="rec-confirm"):
    confirm: bool
