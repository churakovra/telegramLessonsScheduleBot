import asyncio

from aiogram import Bot, Dispatcher

from app.utils.logger import setup_logger
from app.config.settings import BOT_TOKEN
from app.handlers import register_routers
from app.middlewares.setup import setup_middlewares
from app.notifiers.telegram_notifier import TelegramNotifier

logger = setup_logger("bot")


async def main():
    bot = Bot(BOT_TOKEN)
    logger.info("Setup Bot")

    notifier = TelegramNotifier(bot)
    dp = Dispatcher()
    setup_middlewares(dp)
    register_routers(dp)
    dp["notifier"] = notifier
    logger.info("Setup middlewares & dispatcher")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
