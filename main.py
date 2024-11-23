import asyncio
import logging
import sys

import aiogram.types
from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from config import Config
from dt_useful import weekdays
from message_templates import Strings as str

dp = Dispatcher()


@dp.message(Command('set_lesson'))
async def set_lesson(message: Message):
    message_text = str.GREETING
    branch_markup = get_set_types_markup()
    await message.answer(text=message_text, reply_markup=branch_markup)


@dp.callback_query(F.data.startswith('branch_'))
async def get_branch_handler(callback: CallbackQuery):
    match callback.data:
        case str.CALLBACK_BRANCH_DAYS:
            await send_select_day_message(callback)
        case str.CALLBACK_BRANCH_MANUAL:
            await send_set_manual_message(callback)


@dp.callback_query(F.data.startswith('day_'))
async def get_daily_schedule_handler(callback: CallbackQuery):
    pass

async def get_day_schedule(callback_data: str | None):
    pass


async def send_select_day_message(callback: CallbackQuery):
    message_text = str.WEEKDAY
    weekdays_markup = get_weekdays_markup()
    await callback.message.edit_text(text=message_text, reply_markup=weekdays_markup)
    await callback.answer()


async def send_set_manual_message(callback: CallbackQuery):
    message_text = str.SET_MANUAL
    await callback.message.edit_text(text=message_text)
    await callback.answer()


def get_set_types_markup() -> InlineKeyboardMarkup:
    days_bt = InlineKeyboardButton(text=str.BRANCH_DAYS, callback_data=str.CALLBACK_BRANCH_DAYS)
    manual_bt = InlineKeyboardButton(text=str.BRANCH_MANUAL, callback_data=str.CALLBACK_BRANCH_MANUAL)
    markup = InlineKeyboardMarkup(inline_keyboard=[[days_bt, manual_bt]])
    return markup


def get_weekdays_markup() -> InlineKeyboardMarkup:
    keyboard_rows = []
    for items in weekdays.items():
        button = aiogram.types.InlineKeyboardButton(text=items[1], callback_data=f'day_{items[0]}')
        keyboard_rows.append([button])
    markup = aiogram.types.InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    return markup


async def main() -> None:
    bot = Bot(token=Config.TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
