from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.orm import Session

from app.enums.bot_values import UserRoles
from app.services.user_service import UserService
from app.utils.bot_strings import bot_strings as bt

router = Router()


@router.message(Command("start"))
async def add_new_user(message: Message, session: Session):
    username = message.from_user.username
    firstname = message.from_user.first_name
    lastname = message.from_user.last_name
    chat_id = message.from_user.id

    user_service = UserService(session)
    user_service.register_user(
        username=username,
        firstname=firstname,
        lastname=lastname,
        role=UserRoles.STUDENT,
        chat_id=chat_id
    )

    await message.answer(text=bt.GREETING.format(firstname))
