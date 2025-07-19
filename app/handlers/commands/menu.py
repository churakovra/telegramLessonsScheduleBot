from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import UserService
from app.utils.bot_strings import BotStrings
from app.utils.config.logger import setup_logger
from app.utils.exceptions.user_exceptions import UserNotFoundException, UserUnknownRoleException
from app.utils.keyboards.main_menu_markup import get_main_menu_markup

router = Router()

logger = setup_logger()


@router.message(Command("menu"))
async def send_menu_message(
        message: Message,
        session: AsyncSession
):
    logger.debug("in send_menu_message def")
    username = message.from_user.username
    try:
        user_service = UserService(session)
        user = await user_service.get_user(username)
        markup = get_main_menu_markup(user)
        logger.debug(f"Got markup, {str(markup)}")
        await message.answer(
            text=BotStrings.MENU.format(username),
            reply_markup=markup
        )
    except (UserNotFoundException, UserUnknownRoleException) as e:
        await message.answer(e.message)
