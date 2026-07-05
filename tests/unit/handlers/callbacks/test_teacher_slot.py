from datetime import UTC, datetime
from types import SimpleNamespace
from uuid import uuid4

from app.handlers.callbacks.teacher.slot import clear_slots, list_slots
from app.keyboard.callback_factories.slot import SlotListCallback, SlotsClearCallback
from app.message.utils import slots_to_reply
from app.schemas.slot import SlotDTO
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import WeekFlag


def make_callback(mocker):
    return SimpleNamespace(
        from_user=SimpleNamespace(username="teacher-login"),
        message=SimpleNamespace(answer=mocker.AsyncMock()),
        answer=mocker.AsyncMock(),
    )


def make_slot(*, teacher_uuid):
    now = datetime(2026, 7, 1, 10, 0, tzinfo=UTC)
    return SlotDTO(
        id=1,
        uuid=uuid4(),
        uuid_teacher=teacher_uuid,
        dt_start=datetime(2026, 7, 6, 10, 0, tzinfo=UTC),
        dt_add=now,
        uuid_student=None,
        dt_spot=None,
        created_at=now,
        last_updated_at=now,
    )


async def test_list_slots_returns_schedule_text_with_resend_action(mocker):
    teacher_uuid = uuid4()
    slot = make_slot(teacher_uuid=teacher_uuid)
    callback = make_callback(mocker)
    services = SimpleNamespace(
        teacher=SimpleNamespace(
            get_teacher=mocker.AsyncMock(return_value=SimpleNamespace(uuid=teacher_uuid))
        ),
        slot=SimpleNamespace(get_slots=mocker.AsyncMock(return_value=[slot])),
    )

    await list_slots(
        callback,
        SlotListCallback(week_flag=WeekFlag.CURRENT),
        services,
    )

    services.teacher.get_teacher.assert_awaited_once_with("teacher-login")
    services.slot.get_slots.assert_awaited_once_with(teacher_uuid, WeekFlag.CURRENT)
    callback.message.answer.assert_awaited_once()
    assert callback.message.answer.await_args.kwargs["text"] == (
        f"{BotStrings.Teacher.SLOTS_LIST}\n\n{slots_to_reply([slot])}"
    )
    assert callback.message.answer.await_args.kwargs["reply_markup"] is not None
    callback.answer.assert_awaited_once()


async def test_clear_slots_deletes_free_slots_for_selected_week(mocker):
    teacher_uuid = uuid4()
    callback = make_callback(mocker)
    services = SimpleNamespace(
        teacher=SimpleNamespace(
            get_teacher=mocker.AsyncMock(return_value=SimpleNamespace(uuid=teacher_uuid))
        ),
        slot=SimpleNamespace(delete_free_slots=mocker.AsyncMock(return_value=3)),
    )

    await clear_slots(
        callback,
        SlotsClearCallback(week_flag=WeekFlag.NEXT),
        services,
    )

    services.teacher.get_teacher.assert_awaited_once_with("teacher-login")
    services.slot.delete_free_slots.assert_awaited_once_with(
        teacher_uuid,
        WeekFlag.NEXT,
    )
    callback.message.answer.assert_awaited_once()
    assert callback.message.answer.await_args.kwargs["text"] == (
        BotStrings.Teacher.SLOTS_CLEAR_SUCCESS.format(count=3)
    )
    assert callback.message.answer.await_args.kwargs["reply_markup"] is not None
    callback.answer.assert_awaited_once()
