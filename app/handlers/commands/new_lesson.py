from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.keyboards.choose_days_markup import get_choose_days_markup
from app.utils.bot_strings import BotStrings

router = Router()


@router.message(Command("new_lesson"))
async def new_lesson(message: Message):
    markup = get_choose_days_markup()
    await message.answer(
        text=BotStrings.GREETING,
        reply_markup=markup
    )
