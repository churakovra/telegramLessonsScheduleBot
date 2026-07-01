from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.keyboard.callback_factories.lesson import (
    LessonDeleteCallback,
    LessonUpdateCallback,
)
from app.keyboard.callback_factories.student import StudentAssignCallback
from app.keyboard.fabric import (
    admin_main_menu,
    admin_sub_menu_temp,
    cancel_markup,
    confirm_action,
    days_for_students,
    entity_operations,
    lesson_buttons,
    lessons_to_assign,
    listed_slots_actions,
    parsed_slots,
    send_slots,
    slot_buttons,
    slots_for_students,
    specify_week,
    specs_to_update,
    student_buttons,
    student_main_menu,
    student_sub_menu_slot,
    success_slot_bind,
    teacher_main_menu,
    teacher_sub_menu_lesson,
    teacher_sub_menu_slot,
    teacher_sub_menu_student,
)
from app.schemas.lesson import LessonDTO
from app.schemas.slot import SlotDTO
from app.schemas.student import StudentDTO
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import WeekFlag


def labels(markup):
    return [button.text for row in markup.rows for button in row.buttons]


def make_lesson(*, teacher_uuid=None, item_id=1):
    now = datetime.now(UTC)
    return LessonDTO(
        id=item_id,
        uuid=uuid4(),
        label=f"Lesson {item_id}",
        duration=60,
        uuid_teacher=teacher_uuid or uuid4(),
        price=1000,
        created_at=now,
        last_updated_at=now,
    )


def make_slot(*, teacher_uuid=None, hour=10, item_id=1):
    now = datetime.now(UTC)
    return SlotDTO(
        id=item_id,
        uuid=uuid4(),
        uuid_teacher=teacher_uuid or uuid4(),
        dt_start=datetime(2026, 6, 22, hour, tzinfo=UTC),
        dt_add=now,
        uuid_student=None,
        dt_spot=None,
        created_at=now,
        last_updated_at=now,
    )


def make_student():
    now = datetime.now(UTC)
    return StudentDTO(
        id=1,
        uuid=uuid4(),
        username="alice",
        firstname="Alice",
        lastname="Smith",
        is_student=True,
        is_teacher=False,
        is_admin=False,
        chat_id=42,
        created_at=now,
        last_updated_at=now,
    )


@pytest.mark.parametrize(
    "factory",
    [
        teacher_main_menu,
        student_main_menu,
        admin_main_menu,
        teacher_sub_menu_student,
        teacher_sub_menu_slot,
        teacher_sub_menu_lesson,
        student_sub_menu_slot,
        admin_sub_menu_temp,
        parsed_slots,
        cancel_markup,
    ],
)
def test_static_keyboards_have_buttons(factory):
    assert labels(factory())


def test_pin_request_controls_are_not_shown():
    assert "Заявки от учеников" not in labels(teacher_main_menu())
    assert "Преподаватели" not in labels(student_main_menu())


def test_teacher_slot_menu_does_not_send_slots_before_listing_schedule():
    assert BotStrings.Menu.SEND_SLOTS not in labels(teacher_sub_menu_slot())
    assert labels(listed_slots_actions(week_flag=WeekFlag.CURRENT)) == [
        BotStrings.Menu.UPDATE,
        BotStrings.Menu.CLEAR_SLOTS,
        BotStrings.Menu.SEND_SLOTS,
        BotStrings.Menu.BACK,
    ]


def test_slot_selection_keyboards():
    teacher_uuid = uuid4()
    slots = [
        make_slot(teacher_uuid=teacher_uuid),
        make_slot(teacher_uuid=teacher_uuid, hour=11, item_id=2),
    ]

    assert labels(days_for_students(slots=slots, teacher_uuid=teacher_uuid)) == [
        "Понедельник"
    ]
    assert labels(slots_for_students(slots=slots)) == [
        "13:00",
        "14:00",
        BotStrings.Menu.BACK,
    ]
    assert labels(slot_buttons(slots=slots))[-1] == BotStrings.Menu.BACK


def test_entity_list_and_operation_keyboards_do_not_mutate_inputs():
    student = make_student()
    lesson = make_lesson()
    specs = {"label": "Название"}

    assert labels(student_buttons(students=[student])) == [
        "Alice Smith",
        BotStrings.Menu.BACK,
    ]
    assert labels(lesson_buttons(lessons=[lesson])) == [
        "Lesson 1",
        BotStrings.Menu.BACK,
    ]
    assert BotStrings.Menu.DELETE in labels(
        entity_operations(uuid=student.uuid, entity_type=StudentDTO)
    )
    assert labels(
        specs_to_update(
            lesson_uuid=lesson.uuid,
            specs=specs,
            callback_data_cls=LessonUpdateCallback,
        )
    ) == ["Название", "Всё", BotStrings.Menu.BACK]
    assert specs == {"label": "Название"}


def test_action_keyboards():
    teacher_uuid = uuid4()
    lesson = make_lesson(teacher_uuid=teacher_uuid)
    student_uuid = uuid4()

    assert labels(send_slots(teacher_uuid=teacher_uuid)) == [
        BotStrings.Menu.SEND,
        BotStrings.Menu.MENU,
    ]
    assert labels(success_slot_bind(teacher_uuid=teacher_uuid, student_chat_id=42)) == [
        BotStrings.Menu.BIND_ANOTHER_SLOT,
        BotStrings.Menu.MENU,
    ]
    assert labels(
        specify_week(current_week_callback="current", next_week_callback="next")
    ) == [
        BotStrings.Menu.CURRENT_WEEK,
        BotStrings.Menu.NEXT_WEEK,
        BotStrings.Menu.BACK,
    ]
    assert labels(
        confirm_action(
            LessonDeleteCallback
        )
    ) == [BotStrings.Menu.YES, BotStrings.Menu.NO]
    assert labels(
        lessons_to_assign(
            student_uuid=student_uuid,
            lessons=[lesson],
            assign_callback=StudentAssignCallback,
        )
    ) == ["Lesson 1", BotStrings.Menu.CANCEL]
