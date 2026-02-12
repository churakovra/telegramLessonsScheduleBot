from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.keyboard import markup_type_by_role
from app.keyboard.builder import MarkupBuilder
from app.schemas.user_dto import UserDTO
from app.utils.logger import setup_logger
from app.utils.message_template import main_menu_message

router = Router()

logger = setup_logger(__name__)


@router.message(Command("menu"))
async def send_menu_message(message: Message, user: UserDTO):
    markup = MarkupBuilder.build(keyboard_type=markup_type_by_role[user.role])
    bot_message = main_menu_message(markup)
    await message.answer(**bot_message)
