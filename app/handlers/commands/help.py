from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.message.models import BotMessage
from app.utils.bot_strings import BotStrings

router = Router()


@router.message(Command("help"))
async def send_help(message: Message) -> None:
    await message.answer(**BotMessage(text=BotStrings.Common.HELP).to_aiogram_kwargs())
