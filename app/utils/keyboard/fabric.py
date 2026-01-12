import calendar
from uuid import UUID
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.schemas.lesson_dto import LessonDTO
from app.schemas.slot_dto import SlotDTO
from app.utils.bot_strings import BotStrings
from app.utils.datetime_utils import WEEKDAYS, day_format, time_format_HM
from app.utils.enums.bot_values import OperationType, UserRole, WeekFlag
from app.utils.enums.menu_type import MenuType
from app.utils.exceptions.user_exceptions import UserUnknownRoleException
from app.utils.keyboard.callback_factories.back import Back
from app.utils.keyboard.callback_factories.common import BaseCallback, BaseDelete, BaseUpdate
from app.utils.keyboard.callback_factories.menu import NewMainMenu
from app.utils.keyboard.callback_factories.mixins import SpecifyWeekMixin
from app.utils.keyboard.callback_factories.slots import DaysForStudents, ResendSlots, SendSlots, SlotsForStudents
from app.utils.keyboard.context import MenuContext
from app.utils.keyboard.markups.main_menu import MainMenuDataAdmin, MainMenuDataStudent, MainMenuDataTeacher
from app.utils.keyboard.markups.sub_menu import SubMenuDataAdmin, SubMenuDataStudent, SubMenuDataTeacher



def main_menu_markup(builder: InlineKeyboardBuilder, context: MenuContext) -> InlineKeyboardBuilder:
    role = MenuContext.role
    match role:
        case UserRole.TEACHER:
            menu_data = MainMenuDataTeacher.markup
        case UserRole.STUDENT:
            menu_data = MainMenuDataStudent.student_menu
        case UserRole.ADMIN:
            menu_data = MainMenuDataAdmin.admin_menu
        case _:
            raise UserUnknownRoleException(role=role)

    for menu in menu_data:
        builder.button(text=menu.text, callback_data=menu.callback_data)

    builder.adjust(1)
    return builder


def sub_menu_markup(builder, sub_menu_type: MenuType) -> InlineKeyboardMarkup:
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
        case MenuType.ADMIN_TEMP:
            menu_type = SubMenuDataAdmin.admin_temp
        case _:
            raise ValueError(f"Wrong sub_menu_type {sub_menu_type}")
    for button in menu_type:
        builder.button(text=button.text, callback_data=button.callback_data)
    builder.button(
        text="Назад", callback_data=Back(parent_keyboard="menu_keyboard")
    )
    builder.adjust(1)
    return builder

def is_slots_correct_markup(builder) -> InlineKeyboardMarkup:
    builder.button(
        text=BotStrings.Menu.YES,
        callback_data=BotStrings.Teacher.CALLBACK_SLOTS_CORRECT,
    )
    builder.button(
        text=BotStrings.Menu.NO,
        callback_data=BotStrings.Teacher.CALLBACK_SLOTS_INCORRECT,
    )

    return builder

def send_slots_markup(
    builder, teacher_uuid: UUID, operation_type: OperationType
) -> InlineKeyboardMarkup:
    builder.button(
        text=BotStrings.Menu.SEND,
        callback_data=SendSlots(
            teacher_uuid=teacher_uuid, operation_type=operation_type
        ),
    )
    return builder

def days_for_students_markup(
    builder, slots: list[SlotDTO], teacher_uuid: UUID
) -> InlineKeyboardMarkup:
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
    return builder

def slots_for_students_markup(
    builder, slots: list[SlotDTO], teacher_uuid: UUID
) -> InlineKeyboardMarkup:
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
    return builder

def success_slot_bind_markup(
    builder, teacher_uuid: UUID, student_chat_id: int, role: UserRole, username: str
) -> InlineKeyboardMarkup:
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
    return builder

def specify_week_markup(
    builder, callback_data: type[SpecifyWeekMixin],
) -> InlineKeyboardMarkup:
    builder.button(
        text=BotStrings.Menu.CURRENT_WEEK,
        callback_data=callback_data(week_flag=WeekFlag.CURRENT),
    )
    builder.button(
        text=BotStrings.Menu.NEXT_WEEK,
        callback_data=callback_data(week_flag=WeekFlag.NEXT),
    )

    builder.adjust(2)
    return builder

def lessons_markup(builder, lessons: list[LessonDTO], callback_cls: type[BaseCallback]):
    for lesson in lessons:
        builder.button(
            text=lesson.label, callback_data=callback_cls(uuid=lesson.uuid)
        )
    builder.adjust(1)
    return builder

def confirm_deletion_markup(
    builder, callback_data_cls: type[BaseDelete], callback_data: BaseDelete
) -> InlineKeyboardMarkup:
    builder.button(
        text=BotStrings.Menu.YES,
        callback_data=callback_data_cls(uuid=callback_data.uuid, confirmed=True),
    )
    builder.button(
        text=BotStrings.Menu.NO, callback_data=Back(parent_keyboard="menu_keyboard")
    )
    builder.adjust(2)
    return builder

def specs_to_update_markup(
    builder, 
    lesson_uuid: UUID,
    specs: dict[str, str],
    callback_data_cls: type[BaseUpdate]
) -> InlineKeyboardMarkup:
    specs["all"] = "Всё"
    for spec, label in specs.items():
        builder.button(
            text=label, callback_data=callback_data_cls(uuid=lesson_uuid, spec=spec)
        )
    builder.adjust(1)
    return builder