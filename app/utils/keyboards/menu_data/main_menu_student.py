from dataclasses import dataclass

from app.schemas.button_dto import ButtonDTO
from app.utils.enums.menu_type import MenuType
from app.utils.keyboards.callback_factories.main_menu import MainMenuCallback


@dataclass
class MainMenuDataStudent:
    student_menu = [
        ButtonDTO(
            text="Учителя",
            callback_data=MainMenuCallback(menu_type=MenuType.STUDENT_TEACHER),
        ),
        ButtonDTO(
            text="Занятия",
            callback_data=MainMenuCallback(menu_type=MenuType.STUDENT_SLOT),
        ),
        ButtonDTO(
            text="Предметы",
            callback_data=MainMenuCallback(menu_type=MenuType.STUDENT_LESSON),
        ),
    ]
