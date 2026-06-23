import calendar
from typing import Any

from app.keyboard.callback_factories.lesson import (
    LessonCreateCallback,
    LessonDeleteCallback,
    LessonInfoCallback,
    LessonListCallback,
    LessonUpdateCallback,
)
from app.keyboard.callback_factories.menu import ConfirmMenuCallback, MenuCallback
from app.keyboard.callback_factories.slot import (
    DaysForStudents,
    ResendSlotsCallback,
    SendSlots,
    SlotCreateCallback,
    SlotDeleteCallback,
    SlotInfoCallback,
    SlotListCallback,
    SlotsForStudents,
    SlotUpdateCallback,
)
from app.keyboard.callback_factories.student import (
    StudentAssignCallback,
    StudentCreateCallback,
    StudentDeleteCallback,
    StudentDetachCallback,
    StudentInfoCallback,
    StudentListCallback,
)
from app.keyboard.callback_factories.teacher import TeacherCallback
from app.message.models import MarkupData
from app.schemas.lesson import LessonDTO
from app.schemas.slot import SlotDTO
from app.schemas.student import StudentDTO
from app.utils.bot_strings import BotStrings
from app.utils.datetime_utils import WEEKDAYS, day_format, time_format_HM
from app.utils.enums.bot_values import ActionType
from app.utils.enums.menu_type import MenuType

from ..utils.datetime_utils import full_format_no_sec

EntityCallbackMap = dict[type[Any], dict[str, Any]]

ENTITY_OPERATIONS: EntityCallbackMap = {
    StudentDTO: {
        BotStrings.Menu.ATTACH: StudentAssignCallback,
        BotStrings.Menu.DETACH: StudentDetachCallback,
        BotStrings.Menu.DELETE: StudentDeleteCallback,
    },
    LessonDTO: {
        BotStrings.Menu.UPDATE: LessonUpdateCallback,
        BotStrings.Menu.DELETE: LessonDeleteCallback,
    },
    SlotDTO: {
        BotStrings.Menu.UPDATE: SlotUpdateCallback,
        BotStrings.Menu.DELETE: SlotDeleteCallback,
    },
}


def teacher_main_menu() -> MarkupData:
    return MarkupData.from_row_callbacks(
        ("Ученики", MenuCallback(menu_type=MenuType.TEACHER_STUDENT).pack()),
        ("Окошки", MenuCallback(menu_type=MenuType.TEACHER_SLOT).pack()),
        ("Предметы", MenuCallback(menu_type=MenuType.TEACHER_LESSON).pack()),
    )


def student_main_menu() -> MarkupData:
    return MarkupData.from_row_callbacks(
        ("Преподаватели", MenuCallback(menu_type=MenuType.STUDENT_TEACHER).pack()),
        ("Занятия", MenuCallback(menu_type=MenuType.STUDENT_SLOT).pack()),
    )


def admin_main_menu() -> MarkupData:
    return MarkupData.from_row_callbacks(
        ("Пока командами", MenuCallback(menu_type=MenuType.ADMIN_TEMP).pack()),
    )


def teacher_sub_menu_student() -> MarkupData:
    return MarkupData.from_row_callbacks(
        ("Мои ученики", StudentListCallback().pack()),
        ("Добавить ученика", StudentCreateCallback().pack()),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER).pack()),
    )


def teacher_sub_menu_slot() -> MarkupData:
    return MarkupData.from_row_callbacks(
        ("Моё расписание", SlotListCallback().pack()),
        ("Добавить окошки", SlotCreateCallback().pack()),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER).pack()),
    )


def teacher_sub_menu_lesson() -> MarkupData:
    return MarkupData.from_row_callbacks(
        ("Мои предметы", LessonListCallback().pack()),
        ("Добавить предмет", LessonCreateCallback().pack()),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER).pack()),
    )


def student_sub_menu_teacher() -> MarkupData:
    return MarkupData.from_row_callbacks(
        ("Заглушка", TeacherCallback(action=ActionType.LIST).pack()),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.STUDENT).pack()),
    )


def student_sub_menu_slot() -> MarkupData:
    return MarkupData.from_row_callbacks(
        ("Заглушка", SlotListCallback().pack()),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.STUDENT).pack()),
    )


def admin_sub_menu_temp() -> MarkupData:
    return MarkupData.from_row_callbacks(
        ("Пока командами", MenuCallback(menu_type=MenuType.ADMIN_TEMP).pack()),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.ADMIN).pack()),
    )


def parsed_slots() -> MarkupData:
    return MarkupData.from_row_callbacks(
        (BotStrings.Menu.YES, ConfirmMenuCallback(confirm=True).pack()),
        (BotStrings.Menu.NO, ConfirmMenuCallback(confirm=False).pack()),
    )


def send_slots(*, teacher_uuid: str) -> MarkupData:
    return MarkupData.from_row_callbacks(
        (BotStrings.Menu.SEND, SendSlots(teacher_uuid=teacher_uuid).pack()),
        (BotStrings.Menu.CANCEL, MenuCallback(menu_type=MenuType.TEACHER).pack()),
    )


def days_for_students(*, slots: list[SlotDTO], teacher_uuid: str) -> MarkupData:
    prev_slot_date = None
    rows_data: list[tuple[str, str]] = []
    for slot in slots:
        slot_date = slot.dt_start.date()
        if slot_date != prev_slot_date:
            day_number = calendar.weekday(
                slot_date.year, slot_date.month, slot_date.day
            )
            day_name = WEEKDAYS[day_number][2]
            callback_data = DaysForStudents(
                day=slot_date.strftime(day_format),
                teacher_uuid=teacher_uuid,
            )
            rows_data.append((day_name, callback_data.pack()))
            prev_slot_date = slot_date

    return MarkupData.from_row_callbacks(*rows_data)


def slots_for_students(*, slots: list[SlotDTO]) -> MarkupData:
    rows_data: list[tuple[str, str]] = []
    for slot in slots:
        time_str = slot.dt_start.strftime(time_format_HM)
        rows_data.append((time_str, SlotsForStudents(uuid_slot=slot.uuid).pack()))
    rows_data.append(
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.STUDENT).pack())
    )
    return MarkupData.from_row_callbacks(*rows_data)


def success_slot_bind(*, teacher_uuid: str, student_chat_id: int) -> MarkupData:
    return MarkupData.from_row_callbacks(
        (
            BotStrings.Menu.BIND_ANOTHER_SLOT,
            ResendSlotsCallback(
                teacher_uuid=teacher_uuid,
                student_chat_id=student_chat_id,
            ).pack(),
        ),
        (BotStrings.Menu.MENU, MenuCallback(menu_type=MenuType.STUDENT).pack()),
    )


def specify_week(*, current_week_callback: str, next_week_callback: str) -> MarkupData:
    return MarkupData.from_row_callbacks(
        (BotStrings.Menu.CURRENT_WEEK, current_week_callback),
        (BotStrings.Menu.NEXT_WEEK, next_week_callback),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER_SLOT).pack()),
    )


def confirm_deletion(*, callback_data_cls, uuid: str) -> MarkupData:
    return MarkupData.from_row_callbacks(
        (
            BotStrings.Menu.YES,
            callback_data_cls(uuid=uuid, confirmed=True).pack(),
        ),
        (BotStrings.Menu.NO, MenuCallback(menu_type=MenuType.TEACHER).pack()),
    )


def specs_to_update(
    *, lesson_uuid: str, specs: dict[str, str], callback_data_cls
) -> MarkupData:
    specs = {**specs, "all": "Всё"}
    return MarkupData.from_row_callbacks(
        *[
            (label, callback_data_cls(uuid=lesson_uuid, spec=spec).pack())
            for spec, label in specs.items()
        ],
        (BotStrings.Menu.BACK, LessonListCallback().pack()),
    )


def student_buttons(*, students: list[StudentDTO]) -> MarkupData:
    rows_data = [
        (
            " ".join([student.firstname, student.lastname or ""]),
            StudentInfoCallback(uuid=student.uuid).pack(),
        )
        for student in students
    ]
    rows_data.append(
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER_STUDENT).pack())
    )
    return MarkupData.from_row_callbacks(*rows_data)


def lesson_buttons(*, lessons: list[LessonDTO]) -> MarkupData:
    rows_data = [
        (lesson.label, LessonInfoCallback(uuid=lesson.uuid).pack())
        for lesson in lessons
    ]
    rows_data.append(
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER_LESSON).pack())
    )
    return MarkupData.from_row_callbacks(*rows_data)


def slot_buttons(*, slots: list[SlotDTO]) -> MarkupData:
    rows_data = [
        (
            slot.dt_start.strftime(full_format_no_sec),
            SlotInfoCallback(uuid=slot.uuid).pack(),
        )
        for slot in slots
    ]
    rows_data.append(
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER_SLOT).pack())
    )
    return MarkupData.from_row_callbacks(*rows_data)


def entity_operations(*, uuid, entity_type) -> MarkupData:
    rows_data = [
        (name, allowed_operation(uuid=uuid).pack())
        for name, allowed_operation in ENTITY_OPERATIONS[entity_type].items()
    ]
    rows_data.append(
        (BotStrings.Menu.CANCEL, MenuCallback(menu_type=MenuType.NEW).pack())
    )
    return MarkupData.from_row_callbacks(*rows_data)


def lessons_to_assign(
    *, student_uuid: str, lessons: list[LessonDTO], assign_callback
) -> MarkupData:
    rows_data = [
        (
            lesson.label,
            assign_callback(
                uuid=student_uuid,
                id_lesson=lesson.id,
            ).pack(),
        )
        for lesson in lessons
    ]
    rows_data.append(
        (
            BotStrings.Menu.CANCEL,
            MenuCallback(menu_type=MenuType.TEACHER_STUDENT).pack(),
        )
    )
    return MarkupData.from_row_callbacks(*rows_data)


def cancel_markup() -> MarkupData:
    return MarkupData.from_row_callbacks(
        (BotStrings.Menu.CANCEL, MenuCallback(menu_type=MenuType.CANCEL).pack()),
    )
