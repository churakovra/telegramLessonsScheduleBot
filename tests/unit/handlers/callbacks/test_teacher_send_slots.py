from datetime import UTC, datetime
from types import SimpleNamespace
from uuid import uuid4

from app.handlers.callbacks.teacher.send_slots import (
    handle_callback,
    handle_teacher_send_slots,
)
from app.keyboard.callback_factories.slot import SendSlots
from app.message.models import MessageRecipient
from app.schemas.slot import SlotDTO
from app.utils.bot_strings import BotStrings
from app.utils.exceptions.teacher_exceptions import TeacherStudentsNotFound


def make_callback(mocker, *, username="teacher"):
    return SimpleNamespace(
        from_user=SimpleNamespace(username=username),
        message=SimpleNamespace(answer=mocker.AsyncMock()),
        answer=mocker.AsyncMock(),
    )


def make_slot(*, teacher_uuid):
    return SlotDTO(
        id=1,
        uuid=uuid4(),
        uuid_teacher=teacher_uuid,
        dt_start=datetime(2026, 7, 6, 10, 0, tzinfo=UTC),
        dt_add=datetime(2026, 7, 1, 10, 0, tzinfo=UTC),
        uuid_student=None,
        dt_spot=None,
        created_at=datetime(2026, 7, 1, 10, 0, tzinfo=UTC),
        last_updated_at=datetime(2026, 7, 1, 10, 0, tzinfo=UTC),
    )


def make_services(mocker, *, teacher_uuid, students):
    return SimpleNamespace(
        teacher=SimpleNamespace(
            get_unsigned_students=mocker.AsyncMock(return_value=students),
            get_teacher=mocker.AsyncMock(
                return_value=SimpleNamespace(uuid=teacher_uuid)
            ),
        ),
        slot=SimpleNamespace(
            get_free_slots=mocker.AsyncMock(
                return_value=[make_slot(teacher_uuid=teacher_uuid)]
            ),
        ),
    )


async def test_send_slots_notifies_teacher_with_recipient_count(mocker, valid_student):
    teacher_uuid = uuid4()
    callback = make_callback(mocker)
    services = make_services(
        mocker,
        teacher_uuid=teacher_uuid,
        students=[valid_student],
    )
    sender = SimpleNamespace(send=mocker.AsyncMock())

    await handle_callback(
        callback,
        SendSlots(teacher_uuid=teacher_uuid),
        services,
        sender,
    )

    sender.send.assert_awaited_once()
    assert sender.send.await_args.kwargs["recipients"] == [
        MessageRecipient(chat_id=valid_student.chat_id)
    ]
    callback.message.answer.assert_awaited_once()
    assert callback.message.answer.await_args.kwargs["text"] == (
        BotStrings.Teacher.SLOTS_SENT.format(count=1)
    )
    callback.answer.assert_awaited_once()


async def test_send_slots_reports_zero_when_no_eligible_students(mocker):
    teacher_uuid = uuid4()
    callback = make_callback(mocker)
    services = make_services(mocker, teacher_uuid=teacher_uuid, students=[])
    services.teacher.get_unsigned_students.side_effect = TeacherStudentsNotFound(
        teacher_uuid
    )
    sender = SimpleNamespace(send=mocker.AsyncMock())

    await handle_callback(
        callback,
        SendSlots(teacher_uuid=teacher_uuid),
        services,
        sender,
    )

    sender.send.assert_not_awaited()
    callback.message.answer.assert_awaited_once()
    assert callback.message.answer.await_args.kwargs["text"] == (
        BotStrings.Teacher.SLOTS_SENT.format(count=0)
    )
    callback.answer.assert_awaited_once()


async def test_send_slots_from_menu_resolves_teacher(mocker, valid_student):
    teacher_uuid = uuid4()
    callback = make_callback(mocker, username="teacher-login")
    services = make_services(
        mocker,
        teacher_uuid=teacher_uuid,
        students=[valid_student],
    )
    sender = SimpleNamespace(send=mocker.AsyncMock())

    await handle_teacher_send_slots(callback, services, sender)

    services.teacher.get_teacher.assert_awaited_once_with("teacher-login")
    services.teacher.get_unsigned_students.assert_awaited_once_with(teacher_uuid)
    sender.send.assert_awaited_once()
    callback.message.answer.assert_awaited_once()
    assert callback.message.answer.await_args.kwargs["text"] == (
        BotStrings.Teacher.SLOTS_SENT.format(count=1)
    )
    callback.answer.assert_awaited_once()
