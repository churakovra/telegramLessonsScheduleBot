from aiogram.filters.callback_data import CallbackData

from app.utils.enums.bot_values import StatisticsPeriod
from app.utils.enums.menu_type import MenuType


class StatisticsPeriodCallback(CallbackData, prefix="stats-period"):
    period: StatisticsPeriod
    menu_type: MenuType
