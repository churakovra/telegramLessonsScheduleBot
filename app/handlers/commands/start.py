from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import UserService
from app.utils.bot_strings import BotStrings
from app.config.logger import setup_logger
from app.utils.enums.bot_values import UserRole

router = Router()
logger = setup_logger("start")


@router.message(Command("start"))
async def add_new_user(message: Message, session: AsyncSession):
    username = getattr(message.from_user, "username", "") or ""
    first_name = getattr(message.from_user, "first_name", "") or ""
    last_name = getattr(message.from_user, "last_name", None) or None
    id = getattr(message.from_user, "id", 0) or 0

    user_service = UserService(session)
    try:
        await user_service.register_user(
            username=username,
            firstname=first_name,
            lastname=last_name,
            role=UserRole.STUDENT,
            chat_id=id,
        )
    except IntegrityError as e:
        logger.error(e)
    finally:
        await message.answer(text=BotStrings.Common.GREETING.format(user=first_name))
