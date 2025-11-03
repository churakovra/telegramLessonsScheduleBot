from uuid import UUID

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.config.logger import setup_logger
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import UserRole
from app.utils.enums.menu_type import MenuType
from app.utils.exceptions.user_exceptions import UserUnknownRoleException
from app.utils.keyboards.callback_factories.main_menu import MainMenuCallback
from app.utils.keyboards.callback_factories.menu import NewMainMenuCallback
from app.utils.keyboards.callback_factories.send_slots import SendSlotsCallback
from app.utils.keyboards.menu_data.main_menu_admin import MainMenuDataAdmin
from app.utils.keyboards.menu_data.main_menu_student import MainMenuDataStudent
from app.utils.keyboards.menu_data.main_menu_teacher import MainMenuDataTeacher

logger = setup_logger()


class MarkupBuilder:
    @staticmethod
    def main_menu_markup(role: UserRole) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        match role:
            case UserRole.TEACHER:
                menu_data = MainMenuDataTeacher.teacher_menu
            case UserRole.STUDENT:
                menu_data = MainMenuDataStudent.student_menu
            case UserRole.ADMIN:
                menu_data = MainMenuDataAdmin.admin_menu
            case _:
                raise UserUnknownRoleException(role=role)

        for menu in menu_data:
            builder.button(text=menu.text, callback_data=menu.callback_data)
            logger.debug(
                f"get_menu_markup: name={menu.text}; callback_data={menu.callback_data}"
            )

        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def success_slot_bind_markup(teacher_uuid: UUID, role: UserRole, username: str) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text=BotStrings.Menu.BIND_ANOTHER_SLOT,
            callback_data=SendSlotsCallback(teacher_uuid=teacher_uuid),
        )
        builder.button(
            text=BotStrings.Menu.MENU,
            callback_data=NewMainMenuCallback(menu_type=MenuType.NEW, role=role, username=username)
        )
        
        builder.adjust(1)
        return builder.as_markup()
