from aiogram.filters.callback_data import CallbackData

from app.utils.enums.menu_type import MenuType


class BaseMenuCallback(CallbackData, prefix="menu"):
    menu_type: MenuType
