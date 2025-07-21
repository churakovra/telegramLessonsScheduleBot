from dataclasses import dataclass

from app.schemas.button_dto import ButtonDTO
from app.utils.enums.menu_type import MenuType
from app.utils.keyboards.callback_factories.main_menu import MainMenuCallback

@dataclass
class MainMenuDataTeacher:
    teacher_menu = (
        ButtonDTO(
            text="Ученики",
            callback_data=MainMenuCallback(menu_type=MenuType.TEACHER_STUDENT),
        ),
        ButtonDTO(
            text="Окошки",
            callback_data=MainMenuCallback(menu_type=MenuType.TEACHER_SLOT),
        ),
        ButtonDTO(
            text="Уроки",
            callback_data=MainMenuCallback(menu_type=MenuType.TEACHER_LESSON),
        ),
    )