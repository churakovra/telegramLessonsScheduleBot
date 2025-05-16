from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.keyboards.menu_markup import get_menu_markup
from app.models.user_dto import UserDTO
from app.use_cases.register_new_user import register_new_user_use_case
from app.utils.bot_strings import bot_strings as bt

router = Router()


@router.message(Command("start"))
async def add_new_user(message: Message):
    user = UserDTO(
        username=message.from_user.username,
        firstname=message.from_user.first_name,
        lastname=message.from_user.last_name
    )

    await register_new_user_use_case(user)

    await message.answer(
        text=bt.GREETING,
        reply_markup=get_menu_markup()
    )
