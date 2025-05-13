from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.exc import IntegrityError

from app.keyboards.menu_markup import get_menu_markup
from app.models.orm.user import User
from app.services.add_new_user_to_db import add_user
from app.utils.bot_strings import bot_strings as bt

router = Router()


@router.message(Command("start"))
async def add_new_user(message: Message):
    user = User(
        username=message.from_user.username,
        firstname=message.from_user.first_name,
        lastname=message.from_user.last_name
    )
    await message.answer(
        text=bt.GREETING,
        reply_markup=get_menu_markup()
    )
    try:
        await add_user(user)
    except IntegrityError:
        return
