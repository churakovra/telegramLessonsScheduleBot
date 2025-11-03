from aiogram.filters.callback_data import CallbackData

from app.utils.enums.bot_values import UserRole
from app.utils.enums.menu_type import MenuType


class BaseMenu(CallbackData, prefix="base-menu"):
    menu_type: MenuType


class MainMenu(BaseMenu, prefix="main-menu"):
    pass


class SubMenu(BaseMenu, prefix="sub-menu"):
    pass


class NewMainMenu(BaseMenu, prefix="new-main-menu"):
    role: UserRole
    username: str
