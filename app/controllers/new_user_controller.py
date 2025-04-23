from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command

new_user_router = Router()

@new_user_router.message(Command("start"))
async def add_new_user(message: Message):
    text_response = f"Привет, {message.from_user.full_name}"
    await message.answer(
        text=text_response
    )