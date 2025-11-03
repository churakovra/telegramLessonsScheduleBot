from dataclasses import dataclass

from app.schemas.button_dto import ButtonDTO
from app.utils.enums.menu_type import MenuType
from app.utils.keyboards.callback_factories.menu import SubMenu


@dataclass
class SubMenuDataTeacher:
    teacher_student = [
        ButtonDTO(
            text="Добавить ученика",
            callback_data=SubMenu(menu_type=MenuType.TEACHER_STUDENT_ADD),
        ),
        ButtonDTO(
            text="Изменить ученика",
            callback_data=SubMenu(menu_type=MenuType.TEACHER_STUDENT_EDIT),
        ),
        ButtonDTO(
            text="Мои ученики",
            callback_data=SubMenu(menu_type=MenuType.TEACHER_STUDENT_LIST),
        ),
        ButtonDTO(
            text="Удалить ученика",
            callback_data=SubMenu(menu_type=MenuType.TEACHER_STUDENT_DELETE),
        ),
    ]

    teacher_slot = [
        ButtonDTO(
            text="Добавить окошки",
            callback_data=SubMenu(menu_type=MenuType.TEACHER_SLOT_ADD),
        ),
        ButtonDTO(
            text="Изменить окошки",
            callback_data=SubMenu(menu_type=MenuType.TEACHER_SLOT_EDIT),
        ),
        ButtonDTO(
            text="Записать ученика",
            callback_data=SubMenu(menu_type=MenuType.TEACHER_SLOT_SPOT),
        ),
        ButtonDTO(
            text="Мои окошки",
            callback_data=SubMenu(menu_type=MenuType.TEACHER_SLOT_LIST),
        ),
        ButtonDTO(
            text="Удалить окошко",
            callback_data=SubMenu(menu_type=MenuType.TEACHER_SLOT_DELETE),
        ),
    ]

    teacher_lesson = [
        ButtonDTO(
            text="Добавить предмет",
            callback_data=SubMenu(menu_type=MenuType.TEACHER_LESSON_ADD),
        ),
        ButtonDTO(
            text="Изменить предмет",
            callback_data=SubMenu(menu_type=MenuType.TEACHER_LESSON_EDIT),
        ),
        ButtonDTO(
            text="Мои предметы",
            callback_data=SubMenu(menu_type=MenuType.TEACHER_LESSON_LIST),
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
            text="Мои учителя",
            callback_data=SubMenu(menu_type=MenuType.STUDENT_TEACHER_LIST),
        ),
    ]

    student_slot = [
        ButtonDTO(
            text="Мои занятия",
            callback_data=SubMenu(menu_type=MenuType.STUDENT_SLOT_LIST),
        ),
    ]

    student_lesson = [
        ButtonDTO(
            text="Мои предметы",
            callback_data=SubMenu(menu_type=MenuType.STUDENT_LESSON_LIST),
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
