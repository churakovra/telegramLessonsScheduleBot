from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.services.get_user_info_from_db import get_user_info

router = Router()


@router.message(Command("my_info"))
async def get_my_info(message: Message):
    my_info = await get_user_info(message.from_user.username)
    await message.answer(
        text=my_info
    )
