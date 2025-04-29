from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def add_new_user(message: Message):
    text_response = f"Привет, {message.from_user.full_name}"
    await message.answer(
        text=text_response
    )
