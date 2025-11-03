from app.utils.enums.bot_values import UserRole
from app.utils.keyboards.callback_factories.base import BaseMenuCallback


class NewMainMenuCallback(BaseMenuCallback, prefix="fab-new-main-menu"):
    role: UserRole
    username: str