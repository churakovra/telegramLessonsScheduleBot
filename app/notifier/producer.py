import aio_pika
from aio_pika.abc import AbstractChannel, AbstractExchange
from aio_pika.robust_connection import AbstractRobustConnection

from app.config.settings import (
    AMQP_DEFAULT_EXCHANGE,
    AMQP_DEFAULT_EXCHANGE_TYPE,
    AMQP_DEFAULT_ROUTING_KEY,
    AMQP_URL,
)
from app.message.models import MessageEnvelope
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class MessageProducer:
    def __init__(self) -> None:
        self._connection: AbstractRobustConnection | None = None
        self._channel: AbstractChannel | None = None
        self._exchange: AbstractExchange | None = None

    async def start(self) -> None:
        connection = await aio_pika.connect_robust(AMQP_URL)
        channel = await connection.channel()
        exchange = await channel.declare_exchange(
            AMQP_DEFAULT_EXCHANGE, AMQP_DEFAULT_EXCHANGE_TYPE
        )
        self._connection = connection
        self._channel = channel
        self._exchange = exchange
        logger.info("MessageProducer has been started")

    async def produce(self, envelope: MessageEnvelope) -> None:
        if self._exchange is None:
            raise RuntimeError("MessageProducer must be started before producing")

        body = envelope.model_dump_json().encode("utf-8")
        message = aio_pika.Message(body, content_type="application/json")
        await self._exchange.publish(message, routing_key=AMQP_DEFAULT_ROUTING_KEY)

    async def stop(self) -> None:
        if self._channel:
            await self._channel.close()
        if self._connection:
            await self._connection.close()
        logger.info("MessageProducer has been stopped")
