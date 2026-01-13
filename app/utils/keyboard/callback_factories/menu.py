from aiogram.filters.callback_data import CallbackData

from app.utils.enums.menu_type import MenuType


class MenuCallback(CallbackData, prefix="menu"):
    menu_type: MenuType
