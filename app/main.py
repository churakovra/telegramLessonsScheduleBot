import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.config.preferences import BOT_TOKEN
from app.handlers import register_routers


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    register_routers(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
