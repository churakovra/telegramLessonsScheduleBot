from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import UserService
from app.utils.exceptions.user_exceptions import (
    UserNotFoundException,
    UserUnknownRoleException,
)
from app.keyboard import markup_type_by_role
from app.keyboard.builder import MarkupBuilder
from app.utils.logger import setup_logger
from app.utils.message_template import main_menu_message

router = Router()

logger = setup_logger(__name__)

@router.message(Command("menu"))
async def send_menu_message(message: Message, session: AsyncSession):
    username = message.from_user.username
    try:
        user_service = UserService(session)
        user = await user_service.get_user(username)
        markup = MarkupBuilder.build(keyboard_type=markup_type_by_role[user.role])
        bot_message = main_menu_message(user.firstname, markup)
        await message.answer(**bot_message)
    except (UserNotFoundException, UserUnknownRoleException) as e:
        await message.answer(e.message)
