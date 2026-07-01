import calendar
from typing import Any

from app.keyboard.callback_factories.admin import AdminDashboardCallback
from app.keyboard.callback_factories.feedback import (
    FeedbackCallback,
    FeedbackCommentCallback,
    TeacherFeedbackListCallback,
)
from app.keyboard.callback_factories.lesson import (
    LessonCreateCallback,
    LessonDeleteCallback,
    LessonInfoCallback,
    LessonListCallback,
    LessonUpdateCallback,
)
from app.keyboard.callback_factories.menu import ConfirmMenuCallback, MenuCallback
from app.keyboard.callback_factories.notification import (
    NotificationCreateCallback,
    NotificationDeleteCallback,
    NotificationListCallback,
)
from app.keyboard.callback_factories.recurrence import (
    RecurrenceConfirmCallback,
    RecurrenceCreateCallback,
    RecurrenceDayCallback,
    RecurrenceDeleteCallback,
    RecurrenceListCallback,
)
from app.keyboard.callback_factories.reschedule import (
    StudentRescheduleCallback,
    StudentRescheduleConfirmCallback,
    TeacherRescheduleDecisionCallback,
    TeacherRescheduleListCallback,
)
from app.keyboard.callback_factories.schedule import (
    StudentScheduleCallback,
    StudentSlotCancelCallback,
    StudentWeeklyScheduleCallback,
)
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
from app.keyboard.callback_factories.statistics import StatisticsPeriodCallback
from app.keyboard.callback_factories.student import (
    StudentAssignCallback,
    StudentCreateCallback,
    StudentDeleteCallback,
    StudentDetachCallback,
    StudentInfoCallback,
    StudentListCallback,
)
from app.message.models import MarkupData
from app.schemas.lesson import LessonDTO
from app.schemas.notification import NotificationDTO
from app.schemas.recurrence import RecurrenceRuleDTO
from app.schemas.reschedule import RescheduleRequestInfoDTO
from app.schemas.slot import SlotDTO
from app.schemas.student import StudentDTO
from app.utils.bot_strings import BotStrings
from app.utils.datetime_utils import WEEKDAYS, day_format, time_format_HM
from app.utils.enums.bot_values import StatisticsPeriod, UserRole
from app.utils.enums.menu_type import MenuType

from ..utils.datetime_utils import full_format_no_sec

WEEKDAY_LABELS = BotStrings.Common.WEEKDAY_LABELS

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
        (
            BotStrings.Menu.NOTIFICATIONS,
            MenuCallback(menu_type=MenuType.TEACHER_NOTIFICATION).pack(),
        ),
        (
            BotStrings.Menu.RESCHEDULE_REQUESTS,
            MenuCallback(menu_type=MenuType.TEACHER_RESCHEDULE).pack(),
        ),
        (
            BotStrings.Menu.STATISTICS,
            MenuCallback(menu_type=MenuType.TEACHER_STATISTICS).pack(),
        ),
    )


def student_main_menu() -> MarkupData:
    return MarkupData.from_row_callbacks(
        ("Занятия", MenuCallback(menu_type=MenuType.STUDENT_SLOT).pack()),
        (
            BotStrings.Menu.STATISTICS,
            MenuCallback(menu_type=MenuType.STUDENT_STATISTICS).pack(),
        ),
    )


def admin_main_menu() -> MarkupData:
    return MarkupData.from_row_callbacks(
        (BotStrings.Menu.ADMIN_DASHBOARD, AdminDashboardCallback().pack()),
    )


def get_main_menu_by_role(role: UserRole) -> "MarkupData | None":
    """Return the main menu markup for a given user role."""
    match role:
        case UserRole.TEACHER:
            return teacher_main_menu()
        case UserRole.STUDENT:
            return student_main_menu()
        case UserRole.ADMIN:
            return admin_main_menu()
        case _:
            return None


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
        (
            BotStrings.Menu.RECURRENCE,
            MenuCallback(menu_type=MenuType.TEACHER_RECURRENCE).pack(),
        ),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER).pack()),
    )


def teacher_sub_menu_lesson() -> MarkupData:
    return MarkupData.from_row_callbacks(
        ("Мои предметы", LessonListCallback().pack()),
        ("Добавить предмет", LessonCreateCallback().pack()),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER).pack()),
    )


def teacher_sub_menu_notification() -> MarkupData:
    return MarkupData.from_row_callbacks(
        (BotStrings.Menu.CREATE_NOTIFICATION, NotificationCreateCallback().pack()),
        (BotStrings.Menu.MY_NOTIFICATIONS, NotificationListCallback().pack()),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER).pack()),
    )


def teacher_sub_menu_statistics() -> MarkupData:
    return MarkupData.from_row_callbacks(
        (
            BotStrings.Menu.FEEDBACK,
            TeacherFeedbackListCallback().pack(),
        ),
        *statistics_period_rows(back_menu_type=MenuType.TEACHER),
    )


def teacher_recurrence_menu() -> MarkupData:
    return MarkupData.from_row_callbacks(
        (BotStrings.Menu.CREATE_RECURRENCE, RecurrenceCreateCallback().pack()),
        (BotStrings.Menu.RECURRENCE, RecurrenceListCallback().pack()),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER_SLOT).pack()),
    )


def teacher_reschedule_menu() -> MarkupData:
    return MarkupData.from_row_callbacks(
        (BotStrings.Menu.RESCHEDULE_REQUESTS, TeacherRescheduleListCallback().pack()),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER).pack()),
    )


def student_sub_menu_slot() -> MarkupData:
    return MarkupData.from_row_callbacks(
        ("Моё расписание", StudentScheduleCallback().pack()),
        (BotStrings.Menu.WEEKLY_SCHEDULE, StudentWeeklyScheduleCallback().pack()),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.STUDENT).pack()),
    )


def student_sub_menu_statistics() -> MarkupData:
    return statistics_period_menu(back_menu_type=MenuType.STUDENT)


def statistics_period_menu(*, back_menu_type: MenuType) -> MarkupData:
    return MarkupData.from_row_callbacks(
        *statistics_period_rows(back_menu_type=back_menu_type),
    )


def statistics_period_rows(*, back_menu_type: MenuType) -> list[tuple[str, str]]:
    return [
        (
            BotStrings.Menu.WEEK,
            StatisticsPeriodCallback(
                period=StatisticsPeriod.WEEK,
                menu_type=back_menu_type,
            ).pack(),
        ),
        (
            BotStrings.Menu.MONTH,
            StatisticsPeriodCallback(
                period=StatisticsPeriod.MONTH,
                menu_type=back_menu_type,
            ).pack(),
        ),
        (
            BotStrings.Menu.YEAR,
            StatisticsPeriodCallback(
                period=StatisticsPeriod.YEAR,
                menu_type=back_menu_type,
            ).pack(),
        ),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=back_menu_type).pack()),
    ]


def admin_sub_menu_temp() -> MarkupData:
    return MarkupData.from_row_callbacks(
        (BotStrings.Menu.ADMIN_DASHBOARD, AdminDashboardCallback().pack()),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.ADMIN).pack()),
    )


def admin_dashboard_menu() -> MarkupData:
    return MarkupData.from_row_callbacks(
        (BotStrings.Menu.REFRESH, AdminDashboardCallback().pack()),
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


def student_schedule_menu(*, slots: list[SlotDTO]) -> MarkupData:
    rows_data = []
    for slot in slots:
        slot_time = slot.dt_start.strftime(full_format_no_sec)
        rows_data.append(
            [
                (
                    f"{BotStrings.Menu.CANCEL_SLOT} {slot_time}",
                    StudentSlotCancelCallback(uuid_slot=slot.uuid).pack(),
                ),
                (
                    BotStrings.Menu.RESCHEDULE_SLOT,
                    StudentRescheduleCallback(slot_uuid=slot.uuid).pack(),
                ),
            ]
        )
    rows_data.append(
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.STUDENT).pack())
    )
    return MarkupData.from_row_callbacks(*rows_data)


def recurrence_days_menu() -> MarkupData:
    return MarkupData.from_row_callbacks(
        *[
            (label, RecurrenceDayCallback(day_of_week=index).pack())
            for index, label in enumerate(WEEKDAY_LABELS)
        ],
        (BotStrings.Menu.CANCEL, MenuCallback(menu_type=MenuType.CANCEL).pack()),
    )


def recurrence_rules_buttons(*, rules: list[RecurrenceRuleDTO]) -> MarkupData:
    rows_data = []
    for rule in rules:
        label = (
            f"{WEEKDAY_LABELS[rule.day_of_week]} "
            f"{rule.time_start:%H:%M}-{rule.time_end:%H:%M}"
        )
        rows_data.append((label, RecurrenceDeleteCallback(uuid=rule.uuid).pack()))
    rows_data.append(
        (
            BotStrings.Menu.BACK,
            MenuCallback(menu_type=MenuType.TEACHER_RECURRENCE).pack(),
        )
    )
    return MarkupData.from_row_callbacks(*rows_data)


def recurrence_confirm_menu() -> MarkupData:
    return MarkupData.from_row_callbacks(
        (BotStrings.Menu.YES, RecurrenceConfirmCallback(confirm=True).pack()),
        (BotStrings.Menu.NO, RecurrenceConfirmCallback(confirm=False).pack()),
    )


def reschedule_confirm_menu() -> MarkupData:
    return MarkupData.from_row_callbacks(
        (BotStrings.Menu.YES, StudentRescheduleConfirmCallback(confirm=True).pack()),
        (BotStrings.Menu.NO, StudentRescheduleConfirmCallback(confirm=False).pack()),
    )


def teacher_reschedule_buttons(
    *, requests: list[RescheduleRequestInfoDTO]
) -> MarkupData:
    rows_data = []
    for request in requests:
        requested = f"{request.requested_date:%d.%m.%Y} {request.requested_time:%H:%M}"
        rows_data.append(
            [
                (
                    f"{BotStrings.Menu.APPROVE}: {request.student_name} {requested}",
                    TeacherRescheduleDecisionCallback(
                        uuid=request.uuid,
                        approve=True,
                    ).pack(),
                ),
                (
                    BotStrings.Menu.REJECT,
                    TeacherRescheduleDecisionCallback(
                        uuid=request.uuid,
                        approve=False,
                    ).pack(),
                ),
            ]
        )
    rows_data.append(
        (
            BotStrings.Menu.BACK,
            MenuCallback(menu_type=MenuType.TEACHER_RESCHEDULE).pack(),
        )
    )
    return MarkupData.from_row_callbacks(*rows_data)


def feedback_rating_menu(*, slot_uuid) -> MarkupData:
    return MarkupData.from_row_callbacks(
        [
            (
                str(rating),
                FeedbackCallback(slot_uuid=slot_uuid, rating=rating).pack(),
            )
            for rating in range(1, 6)
        ]
    )


def feedback_comment_menu(*, slot_uuid, rating: int) -> MarkupData:
    return MarkupData.from_row_callbacks(
        (
            BotStrings.Menu.YES,
            FeedbackCommentCallback(
                slot_uuid=slot_uuid,
                rating=rating,
                add_comment=True,
            ).pack(),
        ),
        (
            BotStrings.Menu.NO,
            FeedbackCommentCallback(
                slot_uuid=slot_uuid,
                rating=rating,
                add_comment=False,
            ).pack(),
        ),
    )


def notification_buttons(*, notifications: list[NotificationDTO]) -> MarkupData:
    rows_data = [
        (
            f"{notification.minutes_before} мин: {notification.text[:32]}",
            NotificationDeleteCallback(uuid=notification.uuid).pack(),
        )
        for notification in notifications
    ]
    rows_data.append(
        (
            BotStrings.Menu.BACK,
            MenuCallback(menu_type=MenuType.TEACHER_NOTIFICATION).pack(),
        )
    )
    return MarkupData.from_row_callbacks(*rows_data)


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
