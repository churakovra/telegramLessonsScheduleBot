from dataclasses import dataclass

from app.schemas.button_dto import ButtonDTO
from app.utils.enums.menu_type import MenuType
from app.utils.keyboards.callback_factories.main_menu import MainMenuCallback


@dataclass
class MainMenuDataAdmin:
    admin_menu = [
        ButtonDTO(
            text="Пока командами",
            callback_data=MainMenuCallback(menu_type=MenuType.ADMIN_TEMP),
        )
    ]
