import calendar
from uuid import UUID

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.schemas.slot_dto import SlotDTO
from app.utils.bot_strings import BotStrings
from app.utils.datetime_utils import WEEKDAYS, day_format, time_format_HM
from app.utils.enums.bot_values import UserRole
from app.utils.enums.menu_type import MenuType
from app.utils.exceptions.user_exceptions import UserUnknownRoleException
from app.utils.keyboards.callback_factories.back import Back
from app.utils.keyboards.callback_factories.menu import NewMainMenu
from app.utils.keyboards.callback_factories.slots import (
    DaysForStudents,
    ResendSlots,
    SendSlots,
    SlotsForStudents,
)
from app.utils.keyboards.menu_data.main_menu import (
    MainMenuDataAdmin,
    MainMenuDataStudent,
    MainMenuDataTeacher,
)
from app.utils.keyboards.menu_data.sub_menu import (
    SubMenuDataAdmin,
    SubMenuDataStudent,
    SubMenuDataTeacher,
)
from app.utils.logger import setup_logger

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
    def sub_menu_markup(sub_menu_type: MenuType) -> InlineKeyboardMarkup:
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
            logger.debug(
                f"get_sub_menu_markup: name={menu.text}; callback_data={menu.callback_data}"
            )
        builder.button(
            text="Назад", callback_data=Back(parent_keyboard="menu_keyboard")
        )
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def is_slots_correct_markup() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text=BotStrings.Menu.YES,
            callback_data=BotStrings.Teacher.CALLBACK_SLOTS_CORRECT,
        )
        builder.button(
            text=BotStrings.Menu.NO,
            callback_data=BotStrings.Teacher.CALLBACK_SLOTS_INCORRECT,
        )

        return builder.as_markup()

    @staticmethod
    def send_slots_markup(teacher_uuid: UUID) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text=BotStrings.Menu.SEND,
            callback_data=SendSlots(teacher_uuid=teacher_uuid),
        )
        return builder.as_markup()

    @staticmethod
    def days_for_students_markup(
        slots: list[SlotDTO], teacher_uuid: UUID
    ) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        prev_slot_date = None
        for slot in slots:
            slot_date = slot.dt_start.date()
            if slot_date != prev_slot_date:
                day_number = calendar.weekday(
                    slot_date.year, slot_date.month, slot_date.day
                )
                day_name = WEEKDAYS[day_number][2]
                builder.button(
                    text=day_name,
                    callback_data=DaysForStudents(
                        day=slot_date.strftime(day_format), teacher_uuid=teacher_uuid
                    ),
                )
                prev_slot_date = slot_date

        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def slots_for_students_markup(
        slots: list[SlotDTO], teacher_uuid: UUID
    ) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for slot in slots:
            time_str = slot.dt_start.strftime(time_format_HM)
            builder.button(
                text=time_str, callback_data=SlotsForStudents(uuid_slot=slot.uuid)
            )
        builder.button(
            text="Назад",
            callback_data=Back(
                parent_keyboard="days_for_students", teacher_uuid=teacher_uuid
            ),
        )
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def success_slot_bind_markup(
        teacher_uuid: UUID, student_chat_id: int, role: UserRole, username: str
    ) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text=BotStrings.Menu.BIND_ANOTHER_SLOT,
            callback_data=ResendSlots(
                teacher_uuid=teacher_uuid, student_chat_id=student_chat_id
            ),
        )
        builder.button(
            text=BotStrings.Menu.MENU,
            callback_data=NewMainMenu(
                menu_type=MenuType.NEW, role=role, username=username
            ),
        )

        builder.adjust(1)
        return builder.as_markup()
