from dataclasses import dataclass

from app.schemas.button_dto import ButtonDTO
from app.utils.enums.menu_type import MenuType
from app.utils.keyboards.callback_factories.sub_menu import SubMenuCallback

@dataclass
class SubMenuDataStudent:
    student_teacher = (
        ButtonDTO(text="Мои учителя", callback_data=SubMenuCallback(menu_type=MenuType.STUDENT_TEACHER_LIST)),
    )

    student_slot = (
        ButtonDTO(text="Мои занятия", callback_data=SubMenuCallback(menu_type=MenuType.STUDENT_SLOT_LIST)),
    )

    student_lesson = (
        ButtonDTO(text="Мои предметы", callback_data=SubMenuCallback(menu_type=MenuType.STUDENT_LESSON_LIST)),
    )
