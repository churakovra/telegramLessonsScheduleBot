from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.utils.config.logger import setup_logger
from app.utils.enums.menu_type import MenuType
from app.utils.keyboards.callback_factories.back import BackCallback
from app.utils.keyboards.menu_data.sub_menu_admin import SubMenuDataAdmin
from app.utils.keyboards.menu_data.sub_menu_student import SubMenuDataStudent
from app.utils.keyboards.menu_data.sub_menu_teacher import SubMenuDataTeacher

logger = setup_logger()


def get_sub_menu_markup(sub_menu_type: MenuType) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    logger.debug(f"in get_sub_menu_markup, sub_menu_type={sub_menu_type}")
    match sub_menu_type:
        case MenuType.TEACHER_STUDENT:
            menu_type = SubMenuDataTeacher.teacher_student
        case MenuType.TEACHER_SLOT:
            menu_type = SubMenuDataTeacher.teacher_slot
        case MenuType.TEACHER_LESSON:
            menu_type = SubMenuDataTeacher.teacher_lesson
        case MenuType.STUDENT_TEACHER:
            menu_type = SubMenuDataStudent.student_teacher
        case MenuType.STUDENT_SLOT:
            menu_type = SubMenuDataStudent.student_slot
        case MenuType.STUDENT_LESSON:
            menu_type = SubMenuDataStudent.student_lesson
        case MenuType.ADMIN_TEMP:
            menu_type = SubMenuDataAdmin.admin_temp
        case _:
            raise ValueError(f"Wrong sub_menu_type {sub_menu_type}")
    for menu in menu_type:
        builder.button(text=menu.text, callback_data=menu.callback_data)
        logger.debug(f"get_sub_menu_markup: name={menu.text}; callback_data={menu.callback_data}")
    builder.button(
        text="Назад",
        callback_data=BackCallback(parent_keyboard="menu_keyboard")
    )
    builder.adjust(1)
    return builder.as_markup()
