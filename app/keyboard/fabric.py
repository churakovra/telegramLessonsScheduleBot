import calendar

from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.keyboard.callback_factories.lesson import LessonCallback
from app.keyboard.callback_factories.student import StudentCallback
from app.keyboard.callback_factories.teacher import TeacherCallback
from app.utils.bot_strings import BotStrings
from app.utils.datetime_utils import WEEKDAYS, day_format, time_format_HM
from app.utils.enums.bot_values import ActionType, WeekFlag
from app.utils.enums.menu_type import MenuType
from app.keyboard.callback_factories.menu import MenuCallback
from app.keyboard.callback_factories.slot import (
    DaysForStudents,
    ResendSlots,
    SendSlots,
    SlotCallback,
    SlotsForStudents,
)
from app.keyboard.context import (
    ConfirmDeletionKeyboardContext,
    DaysForStudentsKeyboardContext,
    LessonOperationKeyboardContext,
    SendSlotsKeyboardContext,
    SlotsForStudentsKeyboardContext,
    SpecifyWeekKeyboardContext,
    SpecsToUpdateKeyboardContext,
    SuccessSlotBindKeyboardContext,
)


def teacher_main_menu(
    builder: InlineKeyboardBuilder, *args, **kwargs
) -> InlineKeyboardBuilder:
    buttons = [
        ("Ученики", MenuCallback(menu_type=MenuType.TEACHER_STUDENT)),
        ("Расписание", MenuCallback(menu_type=MenuType.TEACHER_SLOT)),
        ("Предметы", MenuCallback(menu_type=MenuType.TEACHER_LESSON)),
    ]
    for button_text, callback in buttons:
        builder.button(text=button_text, callback_data=callback)
    builder.adjust(1)
    return builder


def student_main_menu(
    builder: InlineKeyboardBuilder, *args, **kwargs
) -> InlineKeyboardBuilder:
    buttons = [
        ("Преподаватели", MenuCallback(menu_type=MenuType.STUDENT_TEACHER)),
        ("Занятия", MenuCallback(menu_type=MenuType.STUDENT_SLOT)),
    ]
    for button_text, callback in buttons:
        builder.button(text=button_text, callback_data=callback)
    builder.adjust(1)
    return builder


def admin_main_menu(
    builder: InlineKeyboardBuilder, *args, **kwargs
) -> InlineKeyboardBuilder:
    buttons = [
        ("Пока командами", MenuCallback(menu_type=MenuType.ADMIN_TEMP)),
    ]
    for button_text, callback in buttons:
        builder.button(text=button_text, callback_data=callback)
    builder.adjust(1)
    return builder


def teacher_sub_menu_student(
    builder: InlineKeyboardBuilder, *args, **kwargs
) -> InlineKeyboardBuilder:
    buttons = [
        ("Мои ученики", StudentCallback(action=ActionType.LIST)),
        ("Добавить ученика", StudentCallback(action=ActionType.CREATE)),
        ("Изменить ученика", StudentCallback(action=ActionType.UPDATE)),
        ("Удалить ученика", StudentCallback(action=ActionType.DELETE)),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER)),
    ]
    for button_text, callback in buttons:
        builder.button(text=button_text, callback_data=callback)
    builder.adjust(1)
    return builder


def teacher_sub_menu_slot(
    builder: InlineKeyboardBuilder, *args, **kwargs
) -> InlineKeyboardBuilder:
    buttons = [
        ("Моё расписание", SlotCallback(action=ActionType.LIST)),
        ("Добавить окошки", SlotCallback(action=ActionType.CREATE)),
        ("Изменить окошки", SlotCallback(action=ActionType.UPDATE)),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER)),
    ]
    for button_text, callback in buttons:
        builder.button(text=button_text, callback_data=callback)
    builder.adjust(1)
    return builder


def teacher_sub_menu_lesson(
    builder: InlineKeyboardBuilder, *args, **kwargs
) -> InlineKeyboardBuilder:
    buttons = [
        ("Мои предметы", LessonCallback(action=ActionType.LIST)),
        ("Добавить предмет", LessonCallback(action=ActionType.CREATE)),
        ("Изменить предмет", LessonCallback(action=ActionType.UPDATE)),
        ("Удалить предмет", LessonCallback(action=ActionType.DELETE)),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER))
    ]
    for button_text, callback in buttons:
        builder.button(text=button_text, callback_data=callback)
    builder.adjust(1)
    return builder


def student_sub_menu_teacher(
    builder: InlineKeyboardBuilder, *args, **kwargs
) -> InlineKeyboardBuilder:
    buttons = [
        ("Заглушка", TeacherCallback(action=ActionType.LIST)),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.STUDENT)),
    ]
    for button_text, callback in buttons:
        builder.button(text=button_text, callback_data=callback)
    builder.adjust(1)
    return builder


def student_sub_menu_slot(
    builder: InlineKeyboardBuilder, *args, **kwargs
) -> InlineKeyboardBuilder:
    buttons = [
        ("Заглушка", SlotCallback(action=ActionType.LIST)),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.STUDENT)),
    ]
    for button_text, callback in buttons:
        builder.button(text=button_text, callback_data=callback)
    builder.adjust(1)
    return builder


def admin_sub_menu_temp(
    builder: InlineKeyboardBuilder, *args, **kwargs
) -> InlineKeyboardBuilder:
    buttons = [
        ("Пока командами", MenuCallback(menu_type=MenuType.ADMIN_TEMP)),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.ADMIN)),
    ]
    for button_text, callback in buttons:
        builder.button(text=button_text, callback_data=callback)
    builder.adjust(1)
    return builder


def is_slots_correct_markup(builder, *args, **kwargs) -> InlineKeyboardBuilder:
    buttons = [
        (BotStrings.Menu.YES, BotStrings.Teacher.CALLBACK_SLOTS_CORRECT),
        (BotStrings.Menu.NO, BotStrings.Teacher.CALLBACK_SLOTS_INCORRECT)
    ]
    for button_text, callback in buttons:
        builder.button(text=button_text, callback_data=callback)
    builder.adjust(2)
    return builder


def send_slots(
    builder, context: SendSlotsKeyboardContext, *args, **kwargs
) -> InlineKeyboardBuilder:
    buttons = [
        (BotStrings.Menu.SEND, SendSlots(**context)),
        (BotStrings.Menu.CANCEL, MenuCallback(menu_type=MenuType.TEACHER)),
    ]
    for button_text, callback in buttons:
        builder.button(text=button_text, callback_data=callback)
    builder.adjust(1)
    return builder


def days_for_students(
    builder, context: DaysForStudentsKeyboardContext, *args, **kwargs
) -> InlineKeyboardBuilder:
    prev_slot_date = None
    for slot in context.slots:
        slot_date = slot.dt_start.date()
        if slot_date != prev_slot_date:
            day_number = calendar.weekday(
                slot_date.year, slot_date.month, slot_date.day
            )
            day_name = WEEKDAYS[day_number][2]
            builder.button(
                text=day_name,
                callback_data=DaysForStudents(
                    day=slot_date.strftime(day_format),
                    teacher_uuid=context.teacher_uuid,
                ),
            )
            prev_slot_date = slot_date
    builder.adjust(1)
    return builder


def slots_for_students(
    builder, context: SlotsForStudentsKeyboardContext, *args, **kwargs
) -> InlineKeyboardBuilder:
    for slot in context.slots:
        time_str = slot.dt_start.strftime(time_format_HM)
        builder.button(
            text=time_str, callback_data=SlotsForStudents(uuid_slot=slot.uuid)
        )
    builder.adjust(1)
    return builder


def success_slot_bind(
    builder, context: SuccessSlotBindKeyboardContext, *args, **kwargs
) -> InlineKeyboardBuilder:
    buttons = [
        (BotStrings.Menu.BIND_ANOTHER_SLOT, ResendSlots(**context)),
        (BotStrings.Menu.MENU, MenuCallback(menu_type=MenuType.STUDENT))
    ]
    for button_text, callback in buttons:
        builder.button(text=button_text, callback_data=callback)
    builder.adjust(1)
    return builder


def specify_week(
    builder, context: SpecifyWeekKeyboardContext, *args, **kwargs
) -> InlineKeyboardBuilder:
    buttons = [
        (BotStrings.Menu.CURRENT_WEEK, context.callback_data(week_flag=WeekFlag.CURRENT)),
        (BotStrings.Menu.NEXT_WEEK, context.callback_data(week_flag=WeekFlag.NEXT)),
    ]
    for button_text, callback in buttons:
        builder.button(text=button_text, callback_data=callback)
    builder.adjust(2)
    return builder


def lessons_operation(
    builder, context: LessonOperationKeyboardContext, *args, **kwargs
) -> InlineKeyboardBuilder:
    for lesson in context.lessons:
        builder.button(
            text=lesson.label, callback_data=context.callback_cls(uuid=lesson.uuid)
        )
    builder.adjust(1)
    return builder


def confirm_deletion(
    builder, context: ConfirmDeletionKeyboardContext, *args, **kwargs
) -> InlineKeyboardBuilder:
    buttons = [
        (BotStrings.Menu.YES, context.callback_data_cls(uuid=context.callback_data.uuid, confirmed=True)),
        (BotStrings.Menu.NO, MenuCallback(menu_type=MenuType.TEACHER)),
    ]
    for button_text, callback in buttons:
        builder.button(text=button_text, callback_data=callback)
    builder.adjust(2)
    return builder


def specs_to_update(
    builder, context: SpecsToUpdateKeyboardContext, *args, **kwargs
) -> InlineKeyboardBuilder:
    context.specs["all"] = "Всё"
    for spec, label in context.specs.items():
        builder.button(
            text=label,
            callback_data=context.callback_data_cls(
                uuid=context.lesson_uuid, spec=spec
            ),
        )
    builder.adjust(1)
    return builder
