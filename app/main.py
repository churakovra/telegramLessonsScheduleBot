import asyncio

import debugpy
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from app.config.settings import APP_VERSION, BOT_TOKEN, SERVICE_TYPE
from app.handlers import register_routers
from app.middlewares import register_middlewares
from app.notifier import MessageConsumer, MessageProducer, MessageSender
from app.scheduler import NotificationScheduler
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

    sender = MessageSender(producer=producer)
    scheduler = NotificationScheduler(sender=sender)

    dp = Dispatcher(
        producer=producer,
        sender=sender,
    )
    register_middlewares(dp)
    register_routers(dp)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_my_commands(
            [
                BotCommand(command="start", description="Начать работу с ботом"),
                BotCommand(command="menu", description="Открыть главное меню"),
                BotCommand(command="cancel", description="Отменить текущее действие"),
                BotCommand(command="help", description="Помощь и инструкции"),
            ]
        )
        scheduler.start()
        await dp.start_polling(bot)
    finally:
        await scheduler.stop()
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(main())
