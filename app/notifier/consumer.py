import asyncio

import aio_pika
from aio_pika.abc import AbstractIncomingMessage

from app.config.settings import (
    AMQP_DEFAULT_EXCHANGE,
    AMQP_DEFAULT_EXCHANGE_TYPE,
    AMQP_DEFAULT_QUEUE,
    AMQP_DEFAULT_ROUTING_KEY,
    AMQP_URL,
)
from app.message.models import MessageEnvelope
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class MessageConsumer:
    def __init__(self, bot) -> None:
        self.connection = None
        self.channel = None
        self.queue = None
        self.bot = bot

    async def start(self):
        self.connection = await aio_pika.connect_robust(AMQP_URL)
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(
            AMQP_DEFAULT_EXCHANGE, AMQP_DEFAULT_EXCHANGE_TYPE
        )

        self.queue = await self.channel.declare_queue(AMQP_DEFAULT_QUEUE)
        await self.queue.bind(self.exchange, AMQP_DEFAULT_ROUTING_KEY)
        await self.queue.consume(self.on_message)

        logger.info("MessageConsumer has been started")

    async def on_message(self, incoming_msg: AbstractIncomingMessage):
        async with incoming_msg.process():
            envelope = MessageEnvelope.model_validate_json(incoming_msg.body)
            logger.debug(f"Received envelope: {envelope}")

            # Extract aiogram-compatible kwargs
            kwargs = envelope.message.to_aiogram_kwargs()
            recipients = envelope.recipients

            # Send to all recipients concurrently
            await asyncio.gather(
                *[self.bot.send_message(r.chat_id, **kwargs) for r in recipients]
            )

    async def stop(self):
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()
