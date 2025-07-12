from typing import Dict, Any

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.bot_values import UserRoles
from app.middlewares.db_session import DBSessionMiddleware
from app.services.user_service import UserService
from app.utils.bot_strings import bot_strings as bt

router = Router()

@router.message(Command("start"))
async def add_new_user(message: Message, data: dict):
    session: AsyncSession = data["session"]
    new_user = {
        "username": message.from_user.username,
        "firstname": message.from_user.first_name,
        "lastname": message.from_user.last_name,
        "role": UserRoles.STUDENT,
        "chat_id": message.from_user.id
    }

    user_service = UserService(session)
    await user_service.register_user(**new_user)

    await message.answer(text=bt.GREETING.format(new_user["firstname"]))
