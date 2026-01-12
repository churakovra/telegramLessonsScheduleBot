from abc import ABC
from app.schemas.button_dto import ButtonDTO
from app.utils.enums.menu_type import MenuType
from app.utils.keyboard.callback_factories.menu import MainMenu


class BaseMarkupDraft(ABC):
    def __init__(self):
        self.markup: list[ButtonDTO] = None
        self.adjust: int = None



class MainMenuDataTeacher(BaseMarkupDraft):
    markup = [
        ButtonDTO(
            text="Ученики",
            callback_data=MainMenu(menu_type=MenuType.TEACHER_STUDENT),
        ),
        ButtonDTO(
            text="Расписание",
            callback_data=MainMenu(menu_type=MenuType.TEACHER_SLOT),
        ),
        ButtonDTO(
            text="Предметы",
            callback_data=MainMenu(menu_type=MenuType.TEACHER_LESSON),
        ),
    ]
    adjust = 1


class MainMenuDataStudent:
    student_menu = [
        ButtonDTO(
            text="Преподаватели",
            callback_data=MainMenu(menu_type=MenuType.STUDENT_TEACHER),
        ),
        ButtonDTO(
            text="Занятия",
            callback_data=MainMenu(menu_type=MenuType.STUDENT_SLOT),
        ),
    ]


class MainMenuDataAdmin:
    admin_menu = [
        ButtonDTO(
            text="Пока командами",
            callback_data=MainMenu(menu_type=MenuType.ADMIN_TEMP),
        )
    ]
