from aiogram.filters.callback_data import CallbackData


class BaseMenuCallback(CallbackData, prefix="menu"):
    menu_type: str
