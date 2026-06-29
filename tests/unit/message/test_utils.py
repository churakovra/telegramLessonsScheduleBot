from datetime import UTC, datetime
from uuid import uuid4

from app.message.utils import (
    get_lesson_info,
    get_slot_info,
    get_slots_schedule_reply,
    get_student_info,
    slots_to_reply,
)
from app.schemas.lesson import LessonDTO
from app.schemas.slot import SlotDTO
from app.schemas.student import StudentDTO


def lesson(*, teacher_uuid, label="Math", price=1200, item_id=1):
    now = datetime.now(UTC)
    return LessonDTO(
        id=item_id,
        uuid=uuid4(),
        label=label,
        duration=60,
        uuid_teacher=teacher_uuid,
        price=price,
        created_at=now,
        last_updated_at=now,
    )


def slot(*, teacher_uuid, dt_start, student_uuid=None, item_id=1):
    now = datetime.now(UTC)
    return SlotDTO(
        id=item_id,
        uuid=uuid4(),
        uuid_teacher=teacher_uuid,
        dt_start=dt_start,
        dt_add=now,
        uuid_student=student_uuid,
        dt_spot=None,
        created_at=now,
        last_updated_at=now,
    )


def student(*, student_uuid=None, username="student"):
    now = datetime.now(UTC)
    return StudentDTO(
        id=1,
        uuid=student_uuid or uuid4(),
        username=username,
        firstname="Alice",
        lastname="Smith",
        is_student=True,
        is_teacher=False,
        is_admin=False,
        chat_id=42,
        created_at=now,
        last_updated_at=now,
    )


def test_slots_to_reply_groups_times_by_day():
    teacher_uuid = uuid4()
    slots = [
        slot(
            teacher_uuid=teacher_uuid,
            dt_start=datetime(2026, 6, 22, 10, tzinfo=UTC),
        ),
        slot(
            teacher_uuid=teacher_uuid,
            dt_start=datetime(2026, 6, 22, 11, 30, tzinfo=UTC),
            item_id=2,
        ),
    ]

    result = slots_to_reply(slots)

    assert "Понедельник, 22.06.26" in result
    assert "13:00, 14:30" in result


def test_entity_info_formatters():
    teacher_uuid = uuid4()
    student_dto = student()
    lesson_dto = lesson(teacher_uuid=teacher_uuid)
    slot_dto = slot(
        teacher_uuid=teacher_uuid,
        dt_start=datetime(2026, 6, 22, 10, tzinfo=UTC),
    )

    assert get_student_info(student_dto, lessons=[lesson_dto]) == (
        "Имя: Alice Smith\nЛогин: student\nПредметы: Math"
    )
    assert get_lesson_info(lesson_dto) == (
        "*Math*\nДлительность 60 мин\nСтоимость 1200 руб"
    )
    assert "Ученик: Нет" in get_slot_info(slot_dto)


def test_schedule_reply_summarizes_days_and_week():
    teacher_uuid = uuid4()
    student_dto = student(username="alice")
    student_lesson = lesson(teacher_uuid=teacher_uuid, price=1500)
    slots = [
        slot(
            teacher_uuid=teacher_uuid,
            student_uuid=student_dto.uuid,
            dt_start=datetime(2026, 6, 22, 10, tzinfo=UTC),
        ),
        slot(
            teacher_uuid=teacher_uuid,
            dt_start=datetime(2026, 6, 22, 12, tzinfo=UTC),
            item_id=2,
        ),
        slot(
            teacher_uuid=teacher_uuid,
            student_uuid=student_dto.uuid,
            dt_start=datetime(2026, 6, 23, 11, tzinfo=UTC),
            item_id=3,
        ),
    ]

    result = get_slots_schedule_reply(
        slots,
        {student_dto.uuid: student_lesson},
        [student_dto],
    )

    assert "Понедельник 2026-06-22" in result
    assert "Вторник 2026-06-23" in result
    assert result.count("alice") == 2
    assert "Уроков 1, за день 1500" in result
    assert "Итого: ЗАНЯТИЙ 2 ДОХОД 3000" in result


def test_schedule_reply_skips_incomplete_student_data():
    teacher_uuid = uuid4()
    known_student = student()
    unknown_student_uuid = uuid4()
    slots = [
        slot(
            teacher_uuid=teacher_uuid,
            student_uuid=known_student.uuid,
            dt_start=datetime(2026, 6, 22, 10, tzinfo=UTC),
        ),
        slot(
            teacher_uuid=teacher_uuid,
            student_uuid=unknown_student_uuid,
            dt_start=datetime(2026, 6, 22, 11, tzinfo=UTC),
            item_id=2,
        ),
    ]

    result = get_slots_schedule_reply(
        slots,
        {unknown_student_uuid: lesson(teacher_uuid=teacher_uuid)},
        [],
    )

    assert "Итого: ЗАНЯТИЙ 0 ДОХОД 0" in result
