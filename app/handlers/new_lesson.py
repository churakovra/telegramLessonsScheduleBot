from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from app.utils.bot_strings import BotStrings
from app.keyboards.choose_days_markup import get_choose_days_markup

router = Router()

@router.message(Command("new_lesson"))
async def new_lesson(message: Message):
    markup = get_choose_days_markup()
    await message.answer(
        text=BotStrings.GREETING,
        reply_markup=markup
    )