import asyncio
import logging
import sys

from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command
from aiogram.types import Message

import model
from config import Config
from model import *
from strings import Strings as str

dp = Dispatcher()


@dp.message(Command('set_lesson'))
async def set_lesson(message: Message):
    message_text = str.GREETING
    branch_markup = markups.get_set_types_markup()
    await message.answer(text=message_text, reply_markup=branch_markup)


@dp.callback_query(F.data.startswith('branch_'))
async def get_branch_handler(callback: CallbackQuery):
    match callback.data:
        case str.CALLBACK_BRANCH_DAYS:
            await send_select_day_message(callback)
        case str.CALLBACK_BRANCH_MANUAL:
            await send_set_manual_message(callback)


@dp.callback_query(F.data.startswith('day_'))
async def get_day_schedule_handler(callback: CallbackQuery):
    await model.get_day_schedule(day_callback=callback.data, cday=callback.message.date)


async def main() -> None:
    bot = Bot(token=Config.TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
