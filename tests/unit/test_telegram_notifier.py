from unittest.mock import AsyncMock, call

import pytest

from app.notifier.telegram_notifier import TelegramNotifier
from app.schemas.bot_message import BotMessage


@pytest.fixture
def bot_mock():
    return AsyncMock()


@pytest.fixture
def notifier(bot_mock):
    return TelegramNotifier(bot=bot_mock)


@pytest.mark.asyncio
async def test_send_message(notifier, bot_mock):
    bot_message = BotMessage(message_text="Hello!", reply_markup=None)
    chat_id = 12345

    await notifier.send_message(bot_message, chat_id)

    bot_mock.send_message.assert_awaited_once_with(
        chat_id=chat_id,
        text=bot_message.message_text,
        reply_markup=bot_message.reply_markup,
    )


@pytest.mark.asyncio
async def test_send_message_to_users(notifier, bot_mock, valid_student):
    bot_message = BotMessage(message_text="Hi users!", reply_markup="markup")
    users = [
        valid_student,
        valid_student,
        valid_student,
    ]

    await notifier.send_message_to_users(bot_message, users)

    expected_calls = [
        call(
            chat_id=u.chat_id,
            text=bot_message.message_text,
            reply_markup=bot_message.reply_markup,
        )
        for u in users
    ]
    bot_mock.send_message.assert_has_awaits(expected_calls)
    assert bot_mock.send_message.await_count == len(users)
