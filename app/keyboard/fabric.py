import calendar

from aiogram.filters.callback_data import CallbackData
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
    StudentOperationKeyboardContext,
    SuccessSlotBindKeyboardContext,
)


def teacher_main_menu(*args, **kwargs) -> tuple[list, int]:
    buttons = [
        ("Ученики", MenuCallback(menu_type=MenuType.TEACHER_STUDENT)),
        ("Расписание", MenuCallback(menu_type=MenuType.TEACHER_SLOT)),
        ("Предметы", MenuCallback(menu_type=MenuType.TEACHER_LESSON)),
    ]
    adjust = 1
    return buttons, adjust


def student_main_menu(*args, **kwargs) -> tuple[list, int]:
    buttons = [
        ("Преподаватели", MenuCallback(menu_type=MenuType.STUDENT_TEACHER)),
        ("Занятия", MenuCallback(menu_type=MenuType.STUDENT_SLOT)),
    ]
    adjust = 1
    return buttons, adjust


def admin_main_menu(*args, **kwargs) -> tuple[list, int]:
    buttons = [
        ("Пока командами", MenuCallback(menu_type=MenuType.ADMIN_TEMP)),
    ]
    adjust = 1
    return buttons, adjust


def teacher_sub_menu_student(*args, **kwargs) -> tuple[list, int]:
    buttons = [
        ("Мои ученики", StudentCallback(action=ActionType.LIST)),
        ("Добавить ученика", StudentCallback(action=ActionType.CREATE)),
        ("Изменить ученика", StudentCallback(action=ActionType.UPDATE)),
        ("Удалить ученика", StudentCallback(action=ActionType.DELETE)),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER)),
    ]
    adjust = 1
    return buttons, adjust


def teacher_sub_menu_slot(*args, **kwargs) -> tuple[list, int]:
    buttons = [
        ("Моё расписание", SlotCallback(action=ActionType.LIST)),
        ("Добавить окошки", SlotCallback(action=ActionType.CREATE)),
        ("Изменить окошки", SlotCallback(action=ActionType.UPDATE)),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER)),
    ]
    adjust = 1
    return buttons, adjust


def teacher_sub_menu_lesson(*args, **kwargs) -> tuple[list, int]:
    buttons = [
        ("Мои предметы", LessonCallback(action=ActionType.LIST)),
        ("Добавить предмет", LessonCallback(action=ActionType.CREATE)),
        ("Изменить предмет", LessonCallback(action=ActionType.UPDATE)),
        ("Удалить предмет", LessonCallback(action=ActionType.DELETE)),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER)),
    ]
    adjust = 1
    return buttons, adjust


def student_sub_menu_teacher(*args, **kwargs) -> tuple[list, int]:
    buttons = [
        ("Заглушка", TeacherCallback(action=ActionType.LIST)),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.STUDENT)),
    ]
    adjust = 1
    return buttons, adjust


def student_sub_menu_slot(*args, **kwargs) -> tuple[list, int]:
    buttons = [
        ("Заглушка", SlotCallback(action=ActionType.LIST)),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.STUDENT)),
    ]
    adjust = 1
    return buttons, adjust


def admin_sub_menu_temp(*args, **kwargs) -> tuple[list, int]:
    buttons = [
        ("Пока командами", MenuCallback(menu_type=MenuType.ADMIN_TEMP)),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.ADMIN)),
    ]
    adjust = 1
    return buttons, adjust


def is_slots_correct_markup(*args, **kwargs) -> tuple[list, int]:
    buttons = [
        (BotStrings.Menu.YES, BotStrings.Teacher.CALLBACK_SLOTS_CORRECT),
        (BotStrings.Menu.NO, BotStrings.Teacher.CALLBACK_SLOTS_INCORRECT),
    ]
    adjust = 2
    return buttons, adjust


def send_slots(context: SendSlotsKeyboardContext, *args, **kwargs) -> tuple[list, int]:
    buttons = [
        (BotStrings.Menu.SEND, SendSlots(**context)),
        (BotStrings.Menu.CANCEL, MenuCallback(menu_type=MenuType.TEACHER)),
    ]
    adjust = 1
    return buttons, adjust


def days_for_students(
    context: DaysForStudentsKeyboardContext, *args, **kwargs
) -> tuple[list, int]:
    prev_slot_date = None
    buttons = []
    for slot in context.slots:
        slot_date = slot.dt_start.date()
        if slot_date != prev_slot_date:
            day_number = calendar.weekday(
                slot_date.year, slot_date.month, slot_date.day
            )
            day_name = WEEKDAYS[day_number][2]
            callback_data = DaysForStudents(
                day=slot_date.strftime(day_format),
                teacher_uuid=context.teacher_uuid,
            )
            buttons.append((day_name, callback_data))
            prev_slot_date = slot_date
    adjust = 1
    return buttons, adjust


def slots_for_students(
    context: SlotsForStudentsKeyboardContext, *args, **kwargs
) -> tuple[list, int]:
    buttons = []
    for slot in context.slots:
        time_str = slot.dt_start.strftime(time_format_HM)
        buttons.append((time_str, SlotsForStudents(uuid_slot=slot.uuid)))
    adjust = 1
    return buttons, adjust


def success_slot_bind(
    context: SuccessSlotBindKeyboardContext, *args, **kwargs
) -> tuple[list, int]:
    buttons = [
        (BotStrings.Menu.BIND_ANOTHER_SLOT, ResendSlots(**context)),
        (BotStrings.Menu.MENU, MenuCallback(menu_type=MenuType.STUDENT)),
    ]
    adjust = 1
    return buttons, adjust


def specify_week(
    context: SpecifyWeekKeyboardContext, *args, **kwargs
) -> tuple[list, int]:
    buttons = [
        (
            BotStrings.Menu.CURRENT_WEEK,
            context.callback_data(week_flag=WeekFlag.CURRENT),
        ),
        (BotStrings.Menu.NEXT_WEEK, context.callback_data(week_flag=WeekFlag.NEXT)),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER_SLOT)),
    ]
    adjust = 2
    return buttons, adjust


def student_operation(
    context: StudentOperationKeyboardContext, *args, **kwargs
) -> tuple[list, int]:
    buttons = [
        (
            "".join([student.firstname, student.lastname or ""]),
            context.operation_callback_cls(uuid=student.uuid),
        )
        for student in context.students
    ]
    adjust = 1
    return buttons, adjust


def lesson_operation(
    context: LessonOperationKeyboardContext, *args, **kwargs
) -> tuple[list, int]:
    buttons = [
        (lesson.label, context.operation_callback_cls(uuid=lesson.uuid))
        for lesson in context.lessons
    ]
    buttons.append(
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER_LESSON))
    )
    adjust = 1
    return buttons, adjust


def confirm_deletion(
    context: ConfirmDeletionKeyboardContext, *args, **kwargs
) -> tuple[list, int]:
    buttons = [
        (
            BotStrings.Menu.YES,
            context.callback_data_cls(uuid=context.callback_data.uuid, confirmed=True),
        ),
        (BotStrings.Menu.NO, MenuCallback(menu_type=MenuType.TEACHER)),
    ]
    adjust = 2
    return buttons, adjust


def specs_to_update(
    context: SpecsToUpdateKeyboardContext, *args, **kwargs
) -> tuple[list, int]:
    context.specs["all"] = "Всё"
    buttons = [
        (label, context.callback_data_cls(uuid=context.lesson_uuid, spec=spec))
        for spec, label in context.specs.items()
    ]
    buttons.append((BotStrings.Menu.BACK, LessonCallback(action=ActionType.UPDATE)))
    adjust = 1
    return buttons, adjust
