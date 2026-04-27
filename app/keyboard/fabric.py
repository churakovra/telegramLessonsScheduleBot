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
from app.message.models import MarkupData, RowData, ButtonData
from app.schemas.lesson import LessonDTO
from app.schemas.slot import SlotDTO
from app.schemas.student import StudentDTO
from app.utils.bot_strings import BotStrings
from app.utils.datetime_utils import WEEKDAYS, day_format, time_format_HM
from app.utils.enums.bot_values import ActionType, WeekFlag
from app.utils.enums.menu_type import MenuType

from ..utils.datetime_utils import full_format_no_sec


def teacher_main_menu() -> MarkupData:
    return MarkupData(
        rows=[
            RowData(
                buttons=[
                    ButtonData(
                        text="Ученики",
                        callback_data=MenuCallback(
                            menu_type=MenuType.TEACHER_STUDENT
                        ).pack(),
                    )
                ]
            ),
            RowData(
                buttons=[
                    ButtonData(
                        text="Окошки",
                        callback_data=MenuCallback(
                            menu_type=MenuType.TEACHER_SLOT
                        ).pack(),
                    )
                ]
            ),
            RowData(
                buttons=[
                    ButtonData(
                        text="Предметы",
                        callback_data=MenuCallback(
                            menu_type=MenuType.TEACHER_LESSON
                        ).pack(),
                    )
                ]
            ),
        ]
    )


def student_main_menu() -> MarkupData:
    return MarkupData(
        rows=[
            RowData(
                buttons=[
                    ButtonData(
                        text="Преподаватели",
                        callback_data=MenuCallback(
                            menu_type=MenuType.STUDENT_TEACHER
                        ).pack(),
                    )
                ]
            ),
            RowData(
                buttons=[
                    ButtonData(
                        text="Занятия",
                        callback_data=MenuCallback(
                            menu_type=MenuType.STUDENT_SLOT
                        ).pack(),
                    )
                ]
            ),
        ]
    )


def admin_main_menu() -> MarkupData:
    return MarkupData(
        rows=[
            RowData(
                buttons=[
                    ButtonData(
                        text="Пока командами",
                        callback_data=MenuCallback(
                            menu_type=MenuType.ADMIN_TEMP
                        ).pack(),
                    ),
                ]
            ),
        ]
    )


def teacher_sub_menu_student() -> MarkupData:
    return MarkupData(
        rows=[
            RowData(
                buttons=[
                    ButtonData(
                        text="Мои ученики", callback_data=StudentListCallback().pack()
                    )
                ]
            ),
            RowData(
                buttons=[
                    ButtonData(
                        text="Добавить ученика",
                        callback_data=StudentCreateCallback().pack(),
                    )
                ]
            ),
            RowData(
                buttons=[
                    ButtonData(
                        text=BotStrings.Menu.BACK,
                        callback_data=MenuCallback(menu_type=MenuType.TEACHER).pack(),
                    ),
                ]
            ),
        ]
    )


def teacher_sub_menu_slot() -> MarkupData:
    return MarkupData(
        rows=[
            RowData(
                buttons=[
                    ButtonData(
                        text="Моё расписание", callback_data=SlotListCallback().pack()
                    ),
                ]
            ),
            RowData(
                buttons=[
                    ButtonData(
                        text="Добавить окошки",
                        callback_data=SlotCreateCallback().pack(),
                    ),
                ]
            ),
            RowData(
                buttons=[
                    ButtonData(
                        text=BotStrings.Menu.BACK,
                        callback_data=MenuCallback(menu_type=MenuType.TEACHER).pack(),
                    ),
                ]
            ),
        ]
    )


def teacher_sub_menu_lesson() -> MarkupData:
    return MarkupData(
        rows=[
            RowData(
                buttons=[
                    ButtonData(
                        text="Мои предметы", callback_data=LessonListCallback().pack()
                    ),
                ]
            ),
            RowData(
                buttons=[
                    ButtonData(
                        text="Добавить предмет",
                        callback_data=LessonCreateCallback().pack(),
                    ),
                ]
            ),
            RowData(
                buttons=[
                    ButtonData(
                        text=BotStrings.Menu.BACK,
                        callback_data=MenuCallback(menu_type=MenuType.TEACHER).pack(),
                    ),
                ]
            ),
        ]
    )


def student_sub_menu_teacher(context) -> MarkupData:
    return MarkupData(
        rows=[
            RowData(
                buttons=[
                    ButtonData(
                        text="Заглушка",
                        callback_data=TeacherCallback(action=ActionType.LIST).pack(),
                    ),
                ]
            ),
            RowData(
                buttons=[
                    ButtonData(
                        text=BotStrings.Menu.BACK,
                        callback_data=MenuCallback(menu_type=MenuType.STUDENT).pack(),
                    ),
                ]
            ),
        ]
    )


def student_sub_menu_slot(context) -> MarkupData:
    return MarkupData(
        rows=[
            RowData(
                buttons=[
                    ButtonData(
                        text="Заглушка", callback_data=SlotListCallback().pack()
                    ),
                ]
            ),
            RowData(
                buttons=[
                    ButtonData(
                        text=BotStrings.Menu.BACK,
                        callback_data=MenuCallback(menu_type=MenuType.STUDENT).pack(),
                    ),
                ]
            ),
        ]
    )


def admin_sub_menu_temp(context) -> MarkupData:
    return MarkupData(
        rows=[
            RowData(
                buttons=[
                    ButtonData(
                        text="Пока командами",
                        callback_data=MenuCallback(
                            menu_type=MenuType.ADMIN_TEMP
                        ).pack(),
                    ),
                ]
            ),
            RowData(
                buttons=[
                    ButtonData(
                        text=BotStrings.Menu.BACK,
                        callback_data=MenuCallback(menu_type=MenuType.ADMIN).pack(),
                    ),
                ]
            ),
        ]
    )


def parsed_slots(context) -> MarkupData:
    return MarkupData(
        rows=[
            RowData(
                buttons=[
                    ButtonData(
                        text=BotStrings.Menu.YES,
                        callback_data=ConfirmMenuCallback(confirm=True).pack(),
                    ),
                    ButtonData(
                        text=BotStrings.Menu.NO,
                        callback_data=ConfirmMenuCallback(confirm=False).pack(),
                    ),
                ]
            ),
        ]
    )


def send_slots(context) -> MarkupData:
    return MarkupData(
        rows=[
            RowData(
                buttons=[
                    ButtonData(
                        text=BotStrings.Menu.SEND,
                        callback_data=SendSlots(
                            teacher_uuid=context.teacher_uuid
                        ).pack(),
                    ),
                ]
            ),
            RowData(
                buttons=[
                    ButtonData(
                        text=BotStrings.Menu.CANCEL,
                        callback_data=MenuCallback(menu_type=MenuType.TEACHER).pack(),
                    ),
                ]
            ),
        ]
    )


def days_for_students(context) -> MarkupData:
    prev_slot_date = None
    rows: list[RowData] = []
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
            rows.append(
                RowData(
                    buttons=[
                        ButtonData(text=day_name, callback_data=callback_data.pack()),
                    ]
                )
            )
            prev_slot_date = slot_date

    return MarkupData(rows=rows)


def slots_for_students(context) -> MarkupData:
    rows = []
    for slot in context.slots:
        time_str = slot.dt_start.strftime(time_format_HM)
        rows.append(
            RowData(
                buttons=[
                    ButtonData(
                        text=time_str,
                        callback_data=SlotsForStudents(uuid_slot=slot.uuid).pack(),
                    ),
                ]
            )
        )
    rows.append(
        RowData(
            buttons=[
                ButtonData(
                    text=BotStrings.Menu.BACK,
                    callback_data=MenuCallback(menu_type=MenuType.STUDENT).pack(),
                ),
            ]
        )
    )
    return MarkupData(rows=rows)


def success_slot_bind(context) -> MarkupData:
    return MarkupData(
        rows=[
            RowData(
                buttons=[
                    ButtonData(
                        text=BotStrings.Menu.BIND_ANOTHER_SLOT,
                        callback_data=ResendSlotsCallback(
                            teacher_uuid=context.teacher_uuid,
                            student_chat_id=context.student_chat_id,
                        ).pack(),
                    ),
                    ButtonData(
                        text=BotStrings.Menu.MENU,
                        callback_data=MenuCallback(menu_type=MenuType.STUDENT).pack(),
                    ),
                ]
            ),
        ]
    )


def specify_week(context) -> MarkupData:
    return MarkupData(
        rows=[
            RowData(
                buttons=[
                    ButtonData(
                        text=BotStrings.Menu.CURRENT_WEEK,
                        callback_data=context.callback_cls(
                            week_flag=WeekFlag.CURRENT
                        ).pack(),
                    ),
                    ButtonData(
                        text=BotStrings.Menu.NEXT_WEEK,
                        callback_data=context.callback_cls(
                            week_flag=WeekFlag.NEXT
                        ).pack(),
                    ),
                ]
            ),
            RowData(
                buttons=[
                    ButtonData(
                        text=BotStrings.Menu.BACK,
                        callback_data=MenuCallback(
                            menu_type=MenuType.TEACHER_SLOT
                        ).pack(),
                    ),
                ]
            ),
        ]
    )


def confirm_deletion(context) -> MarkupData:
    # TODO think about NO callback. Maybe should use some 'decline callback' and only then in it's handler send menu to user
    return MarkupData(
        rows=[
            RowData(
                buttons=[
                    ButtonData(
                        text=BotStrings.Menu.YES,
                        callback_data=context.callback_data_cls(
                            uuid=context.callback_data.uuid, confirmed=True
                        ).pack(),
                    ),
                    ButtonData(
                        text=BotStrings.Menu.NO,
                        callback_data=MenuCallback(menu_type=MenuType.TEACHER).pack(),
                    ),
                ]
            ),
        ]
    )


def specs_to_update(context) -> MarkupData:
    context.specs["all"] = "Всё"
    return MarkupData(
        rows=[
            RowData(
                buttons=[
                    ButtonData(
                        text=label,
                        callback_data=context.callback_data_cls(
                            uuid=context.lesson_uuid, spec=spec
                        ).pack(),
                    )
                    for spec, label in context.specs.items()
                ]
            ),
            RowData(
                buttons=[
                    ButtonData(
                        text=BotStrings.Menu.BACK,
                        callback_data=LessonListCallback().pack(),
                    ),
                ]
            ),
        ]
    )


def student_buttons(context) -> MarkupData:
    rows = [
        RowData(
            buttons=[
                ButtonData(
                    text=" ".join([student.firstname, student.lastname or ""]),
                    callback_data=StudentInfoCallback(uuid=student.uuid).pack(),
                ),
            ]
        )
        for student in context.students
    ]
    rows.append(
        RowData(
            buttons=[
                ButtonData(
                    text=BotStrings.Menu.BACK,
                    callback_data=MenuCallback(
                        menu_type=MenuType.TEACHER_STUDENT
                    ).pack(),
                ),
            ]
        )
    )
    return MarkupData(rows=rows)


def lesson_buttons(context) -> MarkupData:
    rows = [
        RowData(
            buttons=[
                ButtonData(
                    text=lesson.label,
                    callback_data=LessonInfoCallback(uuid=lesson.uuid).pack(),
                ),
            ]
        )
        for lesson in context.lessons
    ]
    rows.append(
        RowData(
            buttons=[
                ButtonData(
                    text=BotStrings.Menu.BACK,
                    callback_data=MenuCallback(
                        menu_type=MenuType.TEACHER_LESSON
                    ).pack(),
                ),
            ]
        )
    )
    return MarkupData(rows=rows)


def slot_buttons(context) -> MarkupData:
    rows = [
        RowData(
            buttons=[
                ButtonData(
                    text=slot.dt_start.strftime(full_format_no_sec),
                    callback_data=SlotInfoCallback(uuid=slot.uuid).pack(),
                ),
            ]
        )
        for slot in context.slots
    ]
    rows.append(
        RowData(
            buttons=[
                ButtonData(
                    text=BotStrings.Menu.BACK,
                    callback_data=MenuCallback(menu_type=MenuType.TEACHER_SLOT).pack(),
                ),
            ]
        )
    )
    return MarkupData(rows=rows)


def entity_operations(uuid, entity_type) -> MarkupData:
    operations: dict[Any, dict[str, Any]] = {
        type[StudentDTO]: {
            BotStrings.Menu.ATTACH: StudentAssignCallback,
            BotStrings.Menu.DETACH: StudentDetachCallback,
            BotStrings.Menu.DELETE: StudentDeleteCallback,
        },
        type[LessonDTO]: {
            BotStrings.Menu.UPDATE: LessonUpdateCallback,
            BotStrings.Menu.DELETE: LessonDeleteCallback,
        },
        type[SlotDTO]: {
            BotStrings.Menu.UPDATE: SlotUpdateCallback,
            BotStrings.Menu.DELETE: SlotDeleteCallback,
        },
    }
    rows = [
        RowData(
            buttons=[
                ButtonData(
                    text=name, callback_data=allowed_operation(uuid=uuid).pack()
                ),
            ]
        )
        for name, allowed_operation in operations[entity_type].items()
    ]
    rows.append(
        RowData(
            buttons=[
                ButtonData(
                    text=BotStrings.Menu.CANCEL,
                    callback_data=MenuCallback(menu_type=MenuType.NEW).pack(),
                ),
            ]
        )
    )
    return MarkupData(rows=rows)


def lessons_to_assign(context) -> MarkupData:
    rows = [
        RowData(
            buttons=[
                ButtonData(
                    text=lesson.label,
                    callback_data=context.assign_callback(
                        uuid=context.student_uuid,
                        id_lesson=lesson.id,
                    ).pack(),
                ),
            ]
        )
        for lesson in context.lessons
    ]
    rows.append(
        RowData(
            buttons=[
                ButtonData(
                    text=BotStrings.Menu.CANCEL,
                    callback_data=MenuCallback(
                        menu_type=MenuType.TEACHER_STUDENT
                    ).pack(),
                ),
            ]
        )
    )
    return MarkupData(rows=rows)


def cancel_markup() -> MarkupData:
    return MarkupData(
        rows=[
            RowData(
                buttons=[
                    ButtonData(
                        text=BotStrings.Menu.CANCEL,
                        callback_data=MenuCallback(menu_type=MenuType.CANCEL).pack(),
                    ),
                ]
            ),
        ]
    )
