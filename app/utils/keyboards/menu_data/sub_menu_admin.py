from dataclasses import dataclass

from app.schemas.button_dto import ButtonDTO
from app.utils.enums.menu_type import MenuType
from app.utils.keyboards.callback_factories.sub_menu import SubMenuCallback


@dataclass
class SubMenuDataAdmin:
    admin_temp = [
        ButtonDTO(
            text="Пока командой",
            callback_data=SubMenuCallback(menu_type=MenuType.ADMIN_TEMP),
        ),
    ]
