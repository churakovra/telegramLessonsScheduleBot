import calendar

from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.utils.bot_strings import BotStrings
from app.utils.datetime_utils import WEEKDAYS, day_format, time_format_HM
from app.utils.enums.bot_values import WeekFlag
from app.utils.enums.menu_type import MenuType
from app.utils.keyboard.callback_factories.back import Back
from app.utils.keyboard.callback_factories.menu import MenuCallback
from app.utils.keyboard.callback_factories.slots import (
    DaysForStudents,
    ResendSlots,
    SendSlots,
    SlotsForStudents,
)
from app.utils.keyboard.context import (
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
        ("Мои ученики", MenuCallback(menu_type=MenuType.TEACHER_STUDENT_LIST)),
        ("Добавить ученика", MenuCallback(menu_type=MenuType.TEACHER_STUDENT_ADD)),
        ("Изменить ученика", MenuCallback(menu_type=MenuType.TEACHER_STUDENT_UPDATE)),
        ("Удалить ученика", MenuCallback(menu_type=MenuType.TEACHER_STUDENT_DELETE)),
    ]
    for button_text, callback in buttons:
        builder.button(text=button_text, callback_data=callback)
    builder.adjust(1)
    return builder


def teacher_sub_menu_slot(
    builder: InlineKeyboardBuilder, *args, **kwargs
) -> InlineKeyboardBuilder:
    buttons = [
        ("Моё расписание", MenuCallback(menu_type=MenuType.TEACHER_SLOT_LIST)),
        ("Добавить окошки", MenuCallback(menu_type=MenuType.TEACHER_SLOT_ADD)),
        ("Изменить окошки", MenuCallback(menu_type=MenuType.TEACHER_SLOT_UPDATE)),
    ]
    for button_text, callback in buttons:
        builder.button(text=button_text, callback_data=callback)
    builder.adjust(1)
    return builder


def teacher_sub_menu_lesson(
    builder: InlineKeyboardBuilder, *args, **kwargs
) -> InlineKeyboardBuilder:
    buttons = [
        ("Мои предметы", MenuCallback(menu_type=MenuType.TEACHER_LESSON_LIST)),
        ("Добавить предмет", MenuCallback(menu_type=MenuType.TEACHER_LESSON_ADD)),
        ("Изменить предмет", MenuCallback(menu_type=MenuType.TEACHER_LESSON_UPDATE)),
        ("Удалить предмет", MenuCallback(menu_type=MenuType.TEACHER_LESSON_DELETE)),
    ]
    for button_text, callback in buttons:
        builder.button(text=button_text, callback_data=callback)
    builder.adjust(1)
    return builder


def student_sub_menu_teacher(
    builder: InlineKeyboardBuilder, *args, **kwargs
) -> InlineKeyboardBuilder:
    buttons = [
        ("Заглушка", MenuCallback(menu_type=MenuType.STUDENT_TEACHER_LIST)),
    ]
    for button_text, callback in buttons:
        builder.button(text=button_text, callback_data=callback)
    builder.adjust(1)
    return builder


def student_sub_menu_slot(
    builder: InlineKeyboardBuilder, *args, **kwargs
) -> InlineKeyboardBuilder:
    buttons = [
        ("Заглушка", MenuCallback(menu_type=MenuType.STUDENT_SLOT_LIST)),
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
    builder.button(
        text=BotStrings.Menu.SEND,
        callback_data=SendSlots(
            teacher_uuid=context.teacher_uuid, operation_type=context.operation_type
        ),
    )
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
    builder.button(
        text="Назад",
        callback_data=Back(
            parent_keyboard="days_for_students", teacher_uuid=context.teacher_uuid
        ),
    )
    builder.adjust(1)
    return builder


def success_slot_bind(
    builder, context: SuccessSlotBindKeyboardContext, *args, **kwargs
) -> InlineKeyboardBuilder:
    builder.button(
        text=BotStrings.Menu.BIND_ANOTHER_SLOT,
        callback_data=ResendSlots(
            teacher_uuid=context.teacher_uuid, student_chat_id=context.student_chat_id
        ),
    )
    # builder.button(
    #     text=BotStrings.Menu.MENU,
    #     callback_data=MenuCallback(
    #         menu_type=MenuType.NEW, role=context.role, username=context.username
    #     ),
    # )
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
        (BotStrings.Menu.NO, Back(parent_keyboard="menu_keyboard")),
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
