from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import UserService
from app.utils.enums.bot_values import KeyboardType, UserRole
from app.utils.exceptions.user_exceptions import (
    UserNotFoundException,
    UserUnknownRoleException,
)
from app.utils.keyboard.builder import MarkupBuilder
from app.utils.logger import setup_logger
from app.utils.message_template import main_menu_message

router = Router()

logger = setup_logger(__name__)


markup_type_by_role = {
    UserRole.TEACHER: KeyboardType.TEACHER_MAIN,
    UserRole.STUDENT: KeyboardType.STUDENT_MAIN,
    UserRole.ADMIN: KeyboardType.ADMIN_MAIN,
}


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
