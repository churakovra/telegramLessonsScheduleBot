from dataclasses import dataclass

from app.schemas.button_dto import ButtonDTO
from app.utils.enums.menu_type import MenuType
from app.utils.keyboard.callback_factories.menu import SubMenu


@dataclass
class SubMenuDataTeacher:
    teacher_student = [
        ButtonDTO(
            text="Мои ученики",
            callback_data=SubMenu(menu_type=MenuType.TEACHER_STUDENT_LIST),
        ),
        ButtonDTO(
            text="Добавить ученика",
            callback_data=SubMenu(menu_type=MenuType.TEACHER_STUDENT_ADD),
        ),
        ButtonDTO(
            text="Изменить ученика",
            callback_data=SubMenu(menu_type=MenuType.TEACHER_STUDENT_UPDATE),
        ),
        ButtonDTO(
            text="Удалить ученика",
            callback_data=SubMenu(menu_type=MenuType.TEACHER_STUDENT_DELETE),
        ),
    ]

    teacher_slot = [
        ButtonDTO(
            text="Моё расписание",
            callback_data=SubMenu(menu_type=MenuType.TEACHER_SLOT_LIST),
        ),
        ButtonDTO(
            text="Добавить окошки",
            callback_data=SubMenu(menu_type=MenuType.TEACHER_SLOT_ADD),
        ),
        ButtonDTO(
            text="Изменить окошки",
            callback_data=SubMenu(menu_type=MenuType.TEACHER_SLOT_UPDATE),
        ),
    ]

    teacher_lesson = [
        ButtonDTO(
            text="Мои предметы",
            callback_data=SubMenu(menu_type=MenuType.TEACHER_LESSON_LIST),
        ),
        ButtonDTO(
            text="Добавить предмет",
            callback_data=SubMenu(menu_type=MenuType.TEACHER_LESSON_ADD),
        ),
        ButtonDTO(
            text="Изменить предмет",
            callback_data=SubMenu(menu_type=MenuType.TEACHER_LESSON_UPDATE),
        ),
        ButtonDTO(
            text="Удалить предмет",
            callback_data=SubMenu(menu_type=MenuType.TEACHER_LESSON_DELETE),
        ),
    ]


@dataclass
class SubMenuDataStudent:
    student_teacher = [
        ButtonDTO(
            text="Заглушка",
            callback_data=SubMenu(menu_type=MenuType.STUDENT_TEACHER_LIST),
        ),
    ]

    student_slot = [
        ButtonDTO(
            text="Заглушка",
            callback_data=SubMenu(menu_type=MenuType.STUDENT_SLOT_LIST),
        ),
    ]


@dataclass
class SubMenuDataAdmin:
    admin_temp = [
        ButtonDTO(
            text="Пока командой",
            callback_data=SubMenu(menu_type=MenuType.ADMIN_TEMP),
        ),
    ]
