from unittest.mock import AsyncMock, MagicMock, call

import pytest

from app.message.models import BotMessage, MessageEnvelope, MessageRecipient
from app.notifier.consumer import MessageConsumer
from app.notifier.producer import MessageProducer
from app.notifier.sender import MessageSender


async def test_sender_publishes_single_envelope():
    producer = MagicMock()
    producer.produce = AsyncMock()
    sender = MessageSender(producer=producer)
    message = BotMessage(text="Available slots")
    recipients = [MessageRecipient(chat_id=1), MessageRecipient(chat_id=2)]

    await sender.send(message, recipients)

    envelope = producer.produce.await_args.args[0]
    assert envelope == MessageEnvelope(message=message, recipients=recipients)


async def test_sender_sends_directly_to_every_recipient():
    bot = MagicMock()
    bot.send_message = AsyncMock()
    sender = MessageSender(bot=bot)

    await sender.send(
        BotMessage(text="Hello", parse_mode="HTML"),
        [MessageRecipient(chat_id=1), MessageRecipient(chat_id=2)],
    )

    assert bot.send_message.await_args_list == [
        call(1, text="Hello", parse_mode="HTML"),
        call(2, text="Hello", parse_mode="HTML"),
    ]


async def test_sender_requires_transport():
    with pytest.raises(RuntimeError, match="neither producer nor bot"):
        await MessageSender().send(BotMessage(text="Hello"), [])


async def test_send_to_chat_builds_recipient_and_message():
    producer = MagicMock()
    producer.produce = AsyncMock()
    sender = MessageSender(producer=producer)

    await sender.send_to_chat(42, "Hello", parse_mode="Markdown")

    envelope = producer.produce.await_args.args[0]
    assert envelope.message.text == "Hello"
    assert envelope.message.parse_mode == "Markdown"
    assert envelope.recipients == [MessageRecipient(chat_id=42)]


async def test_producer_rejects_messages_before_start():
    producer = MessageProducer()
    envelope = MessageEnvelope(
        message=BotMessage(text="Hello"),
        recipients=[MessageRecipient(chat_id=1)],
    )

    with pytest.raises(RuntimeError, match="must be started"):
        await producer.produce(envelope)


async def test_producer_serializes_and_publishes_envelope():
    producer = MessageProducer()
    producer._exchange = MagicMock()
    producer._exchange.publish = AsyncMock()
    envelope = MessageEnvelope(
        message=BotMessage(text="Hello"),
        recipients=[MessageRecipient(chat_id=1)],
    )

    await producer.produce(envelope)

    message = producer._exchange.publish.await_args.args[0]
    assert MessageEnvelope.model_validate_json(message.body) == envelope
    assert message.content_type == "application/json"


class IncomingMessage:
    def __init__(self, envelope):
        self.body = envelope.model_dump_json().encode()
        self.processed = False

    def process(self):
        return self

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, traceback):
        self.processed = exc is None


async def test_consumer_processes_and_sends_envelope():
    bot = MagicMock()
    bot.send_message = AsyncMock()
    consumer = MessageConsumer(bot)
    incoming = IncomingMessage(
        MessageEnvelope(
            message=BotMessage(text="Hello"),
            recipients=[MessageRecipient(chat_id=1), MessageRecipient(chat_id=2)],
        )
    )

    await consumer.on_message(incoming)

    assert incoming.processed
    assert bot.send_message.await_args_list == [
        call(1, text="Hello", parse_mode=None),
        call(2, text="Hello", parse_mode=None),
    ]
