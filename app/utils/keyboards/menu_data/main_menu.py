from app.schemas.button_dto import ButtonDTO
from app.utils.enums.menu_type import MenuType
from app.utils.keyboards.callback_factories.menu import MainMenuCallback


class MainMenuDataTeacher:
    teacher_menu = [
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
    ]


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


class MainMenuDataAdmin:
    admin_menu = [
        ButtonDTO(
            text="Пока командами",
            callback_data=MainMenuCallback(menu_type=MenuType.ADMIN_TEMP),
        )
    ]
