import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.config.preferences import BOT_TOKEN
from app.controllers.new_lesson_controller import new_lesson_router
from app.controllers.new_user_controller import new_user_router
from app.handlers.new_lesson_day_callback_handler import new_lesson_day_callback


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(new_user_router)
    dp.include_routers(new_lesson_router, new_lesson_day_callback)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
