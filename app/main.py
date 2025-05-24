import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.config.preferences import BOT_TOKEN
from app.handlers import register_routers
from app.notifiers.telegram_notifier import TelegramNotifier


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(BOT_TOKEN)
    notifier = TelegramNotifier(bot)
    dp = Dispatcher()

    register_routers(dp)
    dp["notifier"] = notifier

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
