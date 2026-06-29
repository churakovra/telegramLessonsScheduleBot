import asyncio
from typing import TYPE_CHECKING

from app.message.models import BotMessage, MarkupData, MessageEnvelope, MessageRecipient
from app.utils.logger import setup_logger

if TYPE_CHECKING:
    from aiogram import Bot

    from app.notifier.producer import MessageProducer

logger = setup_logger(__name__)


class MessageSender:
    """Unified message sender that can dispatch via AMQP or directly via Bot."""

    def __init__(
        self, producer: "MessageProducer | None" = None, bot: "Bot | None" = None
    ) -> None:
        self.producer = producer
        self.bot = bot

    async def send(
        self, message: BotMessage, recipients: list[MessageRecipient]
    ) -> None:
        """Send a message to recipients.

        If producer is set, sends via AMQP (to be consumed by a consumer service).
        If bot is set (and no producer), sends directly via aiogram Bot.
        """
        if self.producer is not None:
            envelope = MessageEnvelope(message=message, recipients=recipients)
            await self.producer.produce(envelope)
            return

        if self.bot is None:
            raise RuntimeError("MessageSender has neither producer nor bot configured")

        kwargs = message.to_aiogram_kwargs()
        await asyncio.gather(
            *[
                self.bot.send_message(recipient.chat_id, **kwargs)
                for recipient in recipients
            ]
        )

    async def send_to_chat(
        self,
        chat_id: int,
        text: str,
        markup: MarkupData | None = None,
        parse_mode: str | None = None,
    ) -> None:
        """Convenience helper to send a plain message to a single chat."""
        message = BotMessage(text=text, markup=markup, parse_mode=parse_mode)
        await self.send(message, [MessageRecipient(chat_id=chat_id)])
