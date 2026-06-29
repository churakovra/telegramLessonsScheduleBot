import pytest

from app.handlers.commands.make_teacher import make_teacher_from_student
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import UserRole
from app.utils.exceptions.user_exceptions import UserChangeRoleException, UserNotFoundException


async def test_make_teacher_success(message, command, services):
    await make_teacher_from_student(message, command, services)

    services.user.add_role.assert_awaited_once_with(
        initiator_username='alice',
        username='alice_teacher',
        role=UserRole.TEACHER,
    )

async def test_returns_without_args(message, command, services):
    command.args = None
    await make_teacher_from_student(message, command, services)

    services.user.add_role.assert_not_awaited()
    message.answer.assert_awaited_once_with(
        text=BotStrings.Admin.MAKE_TEACHER_COMMAND_IS_EMPTY,
        parse_mode=None,
    )

@pytest.mark.parametrize(
    "exception",
    [
        UserNotFoundException("alice_teacher", UserRole.TEACHER),
        UserChangeRoleException("alice_teacher", UserRole.TEACHER, "alice"),
    ],
)
async def test_still_work_on_exception(message, command, services, exception):
    services.user.add_role.side_effect = exception
    await make_teacher_from_student(message, command, services)

    message.answer.assert_awaited_once_with(
        text=BotStrings.Admin.MAKE_TEACHER_FAILURE,
        parse_mode=None,
    )