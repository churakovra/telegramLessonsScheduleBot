from aiogram.filters.callback_data import CallbackData
from app.utils.enums.bot_values import WeekFlag


class SpecifyWeekMixin(CallbackData, prefix="specify-week"):
    week_flag: WeekFlag | None = None
