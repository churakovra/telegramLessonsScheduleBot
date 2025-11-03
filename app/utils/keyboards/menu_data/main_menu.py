from app.schemas.button_dto import ButtonDTO
from app.utils.enums.menu_type import MenuType
from app.utils.keyboards.callback_factories.menu import MainMenu


class MainMenuDataTeacher:
    teacher_menu = [
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
