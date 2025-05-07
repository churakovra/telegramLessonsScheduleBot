from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.utils.get_user_info import get_user_info

router = Router()


@router.message(Command("my_info"))
async def get_my_info(message: Message):
    username = message.from_user.username
    user_info = await get_user_info(username)
    await message.answer(
        text=user_info
    )
