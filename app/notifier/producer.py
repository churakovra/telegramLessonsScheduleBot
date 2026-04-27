import aio_pika

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
    def __init__(self):
        self._connection = None
        self._channel = None
        self._exchange = None

    async def start(self):
        self._connection = await aio_pika.connect_robust(AMQP_URL)
        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange(
            AMQP_DEFAULT_EXCHANGE, AMQP_DEFAULT_EXCHANGE_TYPE
        )
        logger.info("MessageProducer has been started")

    async def produce(self, envelope: MessageEnvelope):
        body = envelope.model_dump_json().encode("utf-8")
        message = aio_pika.Message(body, content_type="application/json")
        await self._exchange.publish(message, routing_key=AMQP_DEFAULT_ROUTING_KEY)

    async def stop(self):
        if self._channel:
            await self._channel.close()
        if self._connection:
            await self._connection.close()
        logger.info("MessageProducer has been stopped")
