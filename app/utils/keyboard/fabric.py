import calendar

from aiogram.types import InlineKeyboardButton
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


def teacher_main_menu(builder: InlineKeyboardBuilder) -> InlineKeyboardBuilder:
    builder.add(
        [
            InlineKeyboardButton(
                text="Ученики",
                callback_data=MenuCallback(menu_type=MenuType.TEACHER_STUDENT),
            ),
            InlineKeyboardButton(
                text="Расписание",
                callback_data=MenuCallback(menu_type=MenuType.TEACHER_SLOT),
            ),
            InlineKeyboardButton(
                text="Предметы",
                callback_data=MenuCallback(menu_type=MenuType.TEACHER_LESSON),
            ),
        ]
    )
    builder.adjust(1)
    return builder


def student_main_menu(builder: InlineKeyboardBuilder) -> InlineKeyboardBuilder:
    builder.add(
        [
            InlineKeyboardButton(
                text="Преподаватели",
                callback_data=MenuCallback(menu_type=MenuType.STUDENT_TEACHER),
            ),
            InlineKeyboardButton(
                text="Занятия", callback_data=MenuCallback(menu_type=MenuType.STUDENT_SLOT)
            ),
        ]
    )
    builder.adjust(1)
    return builder


def admin_main_menu(builder: InlineKeyboardBuilder) -> InlineKeyboardBuilder:
    builder.add(
        [
            InlineKeyboardButton(
                text="Пока командами",
                callback_data=MenuCallback(menu_type=MenuType.ADMIN_TEMP),
            ),
        ]
    )
    builder.adjust(1)
    return builder


def teacher_sub_menu_student(builder: InlineKeyboardBuilder) -> InlineKeyboardBuilder:
    builder.add(
        [
            InlineKeyboardButton(
                text="Мои ученики",
                callback_data=MenuCallback(menu_type=MenuType.TEACHER_STUDENT_LIST),
            ),
            InlineKeyboardButton(
                text="Добавить ученика",
                callback_data=MenuCallback(menu_type=MenuType.TEACHER_STUDENT_ADD),
            ),
            InlineKeyboardButton(
                text="Изменить ученика",
                callback_data=MenuCallback(menu_type=MenuType.TEACHER_STUDENT_UPDATE),
            ),
            InlineKeyboardButton(
                text="Удалить ученика",
                callback_data=MenuCallback(menu_type=MenuType.TEACHER_STUDENT_DELETE),
            ),
        ]
    )
    return builder


def teacher_sub_menu_slot(builder: InlineKeyboardBuilder) -> InlineKeyboardBuilder:
    builder.add(
        [
            InlineKeyboardButton(
                text="Моё расписание",
                callback_data=MenuCallback(menu_type=MenuType.TEACHER_SLOT_LIST),
            ),
            InlineKeyboardButton(
                text="Добавить окошки",
                callback_data=MenuCallback(menu_type=MenuType.TEACHER_SLOT_ADD),
            ),
            InlineKeyboardButton(
                text="Изменить окошки",
                callback_data=MenuCallback(menu_type=MenuType.TEACHER_SLOT_UPDATE),
            ),
        ]
    )
    return builder


def teacher_sub_menu_lesson(builder: InlineKeyboardBuilder) -> InlineKeyboardBuilder:
    builder.add(
        [
            InlineKeyboardButton(
                text="Мои предметы",
                callback_data=MenuCallback(menu_type=MenuType.TEACHER_LESSON_LIST),
            ),
            InlineKeyboardButton(
                text="Добавить предмет",
                callback_data=MenuCallback(menu_type=MenuType.TEACHER_LESSON_ADD),
            ),
            InlineKeyboardButton(
                text="Изменить предмет",
                callback_data=MenuCallback(menu_type=MenuType.TEACHER_LESSON_UPDATE),
            ),
            InlineKeyboardButton(
                text="Удалить предмет",
                callback_data=MenuCallback(menu_type=MenuType.TEACHER_LESSON_DELETE),
            ),
        ]
    )
    return builder


def student_sub_menu_teacher(builder: InlineKeyboardBuilder) -> InlineKeyboardBuilder:
    builder.add(
        [
            InlineKeyboardButton(
                text="Заглушка",
                callback_data=MenuCallback(menu_type=MenuType.STUDENT_TEACHER_LIST),
            ),
        ]
    )
    return builder


def student_sub_menu_slot(builder: InlineKeyboardBuilder) -> InlineKeyboardBuilder:
    builder.add(
        [
            InlineKeyboardButton(
                text="Заглушка",
                callback_data=MenuCallback(menu_type=MenuType.STUDENT_SLOT_LIST),
            ),
        ]
    )
    return builder


def admin_sub_menu_temp(builder: InlineKeyboardBuilder) -> InlineKeyboardBuilder:
    builder.add(
        [
            InlineKeyboardButton(
                text="Пока командой",
                callback_data=MenuCallback(menu_type=MenuType.ADMIN_TEMP),
            ),
        ]
    )
    return builder


def is_slots_correct_markup(builder) -> InlineKeyboardBuilder:
    builder.button(
        text=BotStrings.Menu.YES,
        callback_data=BotStrings.Teacher.CALLBACK_SLOTS_CORRECT,
    )
    builder.button(
        text=BotStrings.Menu.NO,
        callback_data=BotStrings.Teacher.CALLBACK_SLOTS_INCORRECT,
    )

    return builder


def send_slots(builder, context: SendSlotsKeyboardContext) -> InlineKeyboardBuilder:
    builder.button(
        text=BotStrings.Menu.SEND,
        callback_data=SendSlots(
            teacher_uuid=context.teacher_uuid, operation_type=context.operation_type
        ),
    )
    return builder


def days_for_students(
    builder, context: DaysForStudentsKeyboardContext
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
    builder, context: SlotsForStudentsKeyboardContext
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
    builder, context: SuccessSlotBindKeyboardContext
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
    builder,
    context: SpecifyWeekKeyboardContext,
) -> InlineKeyboardBuilder:
    builder.button(
        text=BotStrings.Menu.CURRENT_WEEK,
        callback_data=context.callback_data(week_flag=WeekFlag.CURRENT),
    )
    builder.button(
        text=BotStrings.Menu.NEXT_WEEK,
        callback_data=context.callback_data(week_flag=WeekFlag.NEXT),
    )

    builder.adjust(2)
    return builder


def lessons_operation(
    builder, context: LessonOperationKeyboardContext
) -> InlineKeyboardBuilder:
    for lesson in context.lessons:
        builder.button(
            text=lesson.label, callback_data=context.callback_cls(uuid=lesson.uuid)
        )
    builder.adjust(1)
    return builder


def confirm_deletion(
    builder, context: ConfirmDeletionKeyboardContext
) -> InlineKeyboardBuilder:
    builder.button(
        text=BotStrings.Menu.YES,
        callback_data=context.callback_data_cls(
            uuid=context.callback_data.uuid, confirmed=True
        ),
    )
    builder.button(
        text=BotStrings.Menu.NO,
        callback_data=Back(parent_keyboard="menu_keyboard"),
    )
    builder.adjust(2)
    return builder


def specs_to_update(
    builder, context: SpecsToUpdateKeyboardContext
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
