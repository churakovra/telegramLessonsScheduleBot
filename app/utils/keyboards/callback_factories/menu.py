from aiogram.filters.callback_data import CallbackData

from app.utils.enums.bot_values import UserRole
from app.utils.enums.menu_type import MenuType


class BaseMenuCallback(CallbackData, prefix="menu"):
    menu_type: MenuType


class MainMenuCallback(BaseMenuCallback, prefix="fab-main-menu"):
    pass


class SubMenuCallback(BaseMenuCallback, prefix="sub-menu-callback"):
    pass


class NewMainMenuCallback(BaseMenuCallback, prefix="fab-new-main-menu"):
    role: UserRole
    username: str
