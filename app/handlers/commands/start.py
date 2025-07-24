from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import UserService
from app.utils.bot_strings import BotStrings
from app.utils.config.logger import setup_logger
from app.utils.enums.bot_values import UserRoles

router = Router()
logger = setup_logger("start")


@router.message(Command("start"))
async def add_new_user(message: Message, session: AsyncSession):
    new_user = {
        "username": message.from_user.username,
        "firstname": message.from_user.first_name,
        "lastname": message.from_user.last_name,
        "role": UserRoles.STUDENT,
        "chat_id": message.from_user.id
    }

    user_service = UserService(session)
    try:
        await user_service.register_user(**new_user)
    except IntegrityError as e:
        logger.error(e)
    finally:
        await message.answer(text=BotStrings.GREETING.format(new_user["firstname"]))
