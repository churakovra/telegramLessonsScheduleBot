from types import SimpleNamespace
from uuid import uuid4

from app.handlers.states.teacher_student.wait_for_teacher_students import handle_state
from app.message.models import BotMessage, MessageRecipient
from app.utils.bot_strings import BotStrings


def make_message(mocker, text: str = "@student"):
    return SimpleNamespace(text=text, answer=mocker.AsyncMock())


def make_state(mocker, *, teacher_uuid):
    return SimpleNamespace(
        get_data=mocker.AsyncMock(return_value={"teacher_uuid": teacher_uuid}),
        clear=mocker.AsyncMock(),
    )


def make_services(mocker, *, teacher, students, unknown_students=None):
    return SimpleNamespace(
        teacher=SimpleNamespace(
            get_teacher_by_uuid=mocker.AsyncMock(return_value=teacher),
            attach_students=mocker.AsyncMock(),
        ),
        student=SimpleNamespace(
            parse_students=mocker.AsyncMock(
                return_value=(students, unknown_students or [])
            ),
        ),
    )


async def test_attaches_students_and_notifies_them(mocker, valid_teacher, valid_student):
    teacher_uuid = uuid4()
    message = make_message(mocker, text="@test-student")
    state = make_state(mocker, teacher_uuid=teacher_uuid)
    services = make_services(mocker, teacher=valid_teacher, students=[valid_student])
    sender = SimpleNamespace(send=mocker.AsyncMock())

    await handle_state(message, services, state, sender)

    services.teacher.get_teacher_by_uuid.assert_awaited_once_with(
        teacher_uuid=teacher_uuid
    )
    services.student.parse_students.assert_awaited_once_with("@test-student")
    services.teacher.attach_students.assert_awaited_once_with(
        teacher_uuid=teacher_uuid,
        students=[valid_student],
        uuid_lesson=None,
    )
    state.clear.assert_awaited_once()
    sender.send.assert_awaited_once_with(
        message=BotMessage(
            text=BotStrings.Student.ATTACHED_TO_TEACHER.format(
                teacher_name=(
                    f"{valid_teacher.firstname} {valid_teacher.lastname}"
                ),
                teacher_username=valid_teacher.username,
            )
        ),
        recipients=[MessageRecipient(chat_id=valid_student.chat_id)],
    )
    assert message.answer.await_args_list[0].kwargs["text"] == (
        BotStrings.Teacher.TEACHER_STUDENT_ADD_SUCCESS.format(
            student=valid_student.username
        )
    )
    assert message.answer.await_args_list[-1].kwargs["text"] == BotStrings.Common.MENU


async def test_unknown_students_do_not_trigger_notifications(mocker, valid_teacher):
    teacher_uuid = uuid4()
    message = make_message(mocker, text="@missing")
    state = make_state(mocker, teacher_uuid=teacher_uuid)
    services = make_services(
        mocker,
        teacher=valid_teacher,
        students=[],
        unknown_students=["missing"],
    )
    sender = SimpleNamespace(send=mocker.AsyncMock())

    await handle_state(message, services, state, sender)

    services.teacher.attach_students.assert_not_awaited()
    sender.send.assert_not_awaited()
    state.clear.assert_awaited_once()
    assert message.answer.await_args_list[0].kwargs["text"] == (
        BotStrings.Teacher.TEACHER_STUDENT_ADD_UNKNOWN_STUDENT.format(
            student="missing"
        )
    )
    assert message.answer.await_args_list[-1].kwargs["text"] == BotStrings.Common.MENU
