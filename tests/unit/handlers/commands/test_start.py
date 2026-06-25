from app.handlers.commands.start import add_new_user
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import UserRole
from app.utils.exceptions.user_exceptions import UserAlreadyExistsException


async def test_registers_student(message, services):
    await add_new_user(message, services)

    services.user.register_user.assert_awaited_once_with(
        username="alice",
        firstname="Alice",
        lastname="Smith",
        role=UserRole.STUDENT,
        chat_id=42,
    )


async def test_greets_registered_user(message, services):
    await add_new_user(message, services)

    message.answer.assert_awaited_once_with(
        text=BotStrings.Common.GREETING.format(user="Alice"),
        parse_mode=None,
    )


async def test_greets_existing_user(message, services):
    services.user.register_user.side_effect = UserAlreadyExistsException("alice")

    await add_new_user(message, services)

    message.answer.assert_awaited_once_with(
        text=BotStrings.Common.GREETING.format(user="Alice"),
        parse_mode=None,
    )


async def test_requires_telegram_username(message, services):
    message.from_user.username = None

    await add_new_user(message, services)

    services.user.register_user.assert_not_awaited()
    message.answer.assert_awaited_once_with(
        text=BotStrings.User.USERNAME_REQUIRED,
        parse_mode=None,
    )
