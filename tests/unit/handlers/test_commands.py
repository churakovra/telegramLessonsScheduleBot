from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from sqlalchemy.exc import IntegrityError

from app.handlers.commands.make_teacher import make_teacher_from_student
from app.handlers.commands.start import add_new_user
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import UserRole
from app.utils.exceptions.user_exceptions import UserNotFoundException


def make_message(username="alice", first_name="Alice", last_name="Smith"):
    message = MagicMock()
    message.from_user = SimpleNamespace(
        username=username,
        first_name=first_name,
        last_name=last_name,
        id=42,
    )
    message.answer = AsyncMock()
    return message


async def test_start_registers_student_and_answers():
    message = make_message()
    services = MagicMock()
    services.user.register_user = AsyncMock(return_value=uuid4())

    await add_new_user(message, services)

    services.user.register_user.assert_awaited_once_with(
        username="alice",
        firstname="Alice",
        lastname="Smith",
        role=UserRole.STUDENT,
        chat_id=42,
    )
    message.answer.assert_awaited_once_with(
        text=BotStrings.Common.GREETING.format(user="Alice"),
        parse_mode=None,
    )


async def test_start_still_answers_existing_user():
    message = make_message()
    services = MagicMock()
    services.user.register_user = AsyncMock(
        side_effect=IntegrityError("insert", {}, Exception("duplicate"))
    )

    await add_new_user(message, services)

    message.answer.assert_awaited_once()


async def test_make_teacher_rejects_empty_command():
    message = make_message(username="admin")
    services = MagicMock()

    await make_teacher_from_student(message, SimpleNamespace(args=None), services)

    services.user.add_role.assert_not_called()
    message.answer.assert_awaited_once_with(
        text=BotStrings.Admin.MAKE_TEACHER_COMMAND_IS_EMPTY,
        parse_mode=None,
    )


async def test_make_teacher_adds_role():
    message = make_message(username="admin")
    services = MagicMock()
    services.user.add_role = AsyncMock()

    await make_teacher_from_student(message, SimpleNamespace(args=" alice "), services)

    services.user.add_role.assert_awaited_once_with("admin", "alice", UserRole.TEACHER)
    message.answer.assert_awaited_once_with(
        text=BotStrings.Admin.MAKE_TEACHER_SUCCESS.format(user="alice"),
        parse_mode=None,
    )


async def test_make_teacher_reports_domain_failure():
    message = make_message(username="admin")
    services = MagicMock()
    error = UserNotFoundException("alice", UserRole.TEACHER)
    services.user.add_role = AsyncMock(side_effect=error)

    await make_teacher_from_student(message, SimpleNamespace(args="alice"), services)

    kwargs = message.answer.await_args.kwargs
    assert BotStrings.Admin.MAKE_TEACHER_FAILURE in kwargs["text"]
    assert error.message in kwargs["text"]
