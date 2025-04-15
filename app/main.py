import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.config.preferences import BOT_TOKEN


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
