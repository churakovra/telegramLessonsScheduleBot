import asyncio

from aiogram import Bot, Dispatcher
import debugpy

from app.config.settings import APP_VERSION, BOT_TOKEN, SERVICE_TYPE
from app.handlers import register_routers
from app.middlewares import register_middlewares
from app.notifier import MessageConsumer, MessageProducer
from app.utils.enums.common import ServiceType
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

bot = Bot(BOT_TOKEN)
logger.info("Start Bot")


async def main() -> None:

    if SERVICE_TYPE == ServiceType.CONSUMER:
        consumer = MessageConsumer(bot)
        await consumer.start()
        try:
            await asyncio.Future()
        finally:
            await consumer.stop()
        return
    
    if APP_VERSION in ("dev", "qa"):
        debugpy.listen(("0.0.0.0", 5678))

    producer = MessageProducer()
    await producer.start()

    dp = Dispatcher(
        producer=producer,
    )
    register_middlewares(dp)
    register_routers(dp)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(main())
