from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.utils.config.logger import setup_logger
from app.utils.enums.menu_type import MenuType
from app.utils.keyboards.callback_factories.back import BackCallback
from app.utils.keyboards.callback_factories.sub_menu import (
    SubMenuCallback,
    teacher_student,
    teacher_slot,
    teacher_lesson,
    student_teacher,
    student_slot,
    student_lesson,
)

logger = setup_logger()


def get_sub_menu_markup(sub_menu_type: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    logger.debug(f"in get_sub_menu_markup, sub_menu_type={sub_menu_type}")
    match sub_menu_type:
        case MenuType.TEACHER_STUDENT:
            menu_type = teacher_student
        case MenuType.TEACHER_SLOT:
            menu_type = teacher_slot
        case MenuType.TEACHER_LESSON:
            menu_type = teacher_lesson
        case MenuType.STUDENT_TEACHER:
            menu_type = student_teacher
        case MenuType.STUDENT_SLOT:
            menu_type = student_slot
        case MenuType.STUDENT_LESSON:
            menu_type = student_lesson
        case _:
            raise ValueError(f"Wrong sub_menu_type {sub_menu_type}")
    for name, value in menu_type.items():
        builder.button(text=name, callback_data=SubMenuCallback(menu_type=value))
        logger.debug(f"get_sub_menu_markup: name={name}; callback_data={value}")
    builder.button(
        text="Назад",
        callback_data=BackCallback(current_level=sub_menu_type, parent_keyboard="menu_keyboard")
    )
    builder.adjust(1)
    return builder.as_markup()
