from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import UserService
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import UserRole
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.message(Command("start"))
async def add_new_user(message: Message, session: AsyncSession):
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    id = message.from_user.id

    user_service = UserService(session)
    try:
        new_user_uuid = await user_service.register_user(
            username=username,
            firstname=first_name,
            lastname=last_name,
            role=UserRole.STUDENT,
            chat_id=id,
        )
        logger.info(f"New user registeged. User id: {new_user_uuid}")
    except IntegrityError as e:
        logger.error(f"User {username} already registered")
    finally:
        await message.answer(text=BotStrings.Common.GREETING.format(user=first_name))
