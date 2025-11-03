from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.logger import setup_logger
from app.services.user_service import UserService
from app.utils.exceptions.user_exceptions import (
    UserNotFoundException,
    UserUnknownRoleException,
)
from app.utils.keyboards.menu_builder import MarkupBuilder
from app.utils.message_template import MessageTemplate

router = Router()

logger = setup_logger()


@router.message(Command("menu"))
async def send_menu_message(message: Message, session: AsyncSession):
    logger.debug("in send_menu_message def")
    username = getattr(message.from_user, "username", "")
    try:
        user_service = UserService(session)
        user = await user_service.get_user(username)
        markup = MarkupBuilder.main_menu_markup(user.role)
        logger.debug(f"Got markup, {str(markup)}")
        bot_message = MessageTemplate.main_menu_message(user.firstname, markup)
        await message.answer(
            text=bot_message.message_text, reply_markup=bot_message.reply_markup
        )
    except (UserNotFoundException, UserUnknownRoleException) as e:
        await message.answer(e.message)
    finally:
        await message.delete()
