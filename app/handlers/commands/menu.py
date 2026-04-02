from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.message import context, message_builder
from app.message.message import BotMessage
from app.schemas.user import UserDTO
from app.utils.logger import setup_logger

router = Router()

logger = setup_logger(__name__)


@router.message(Command("menu"))
async def send_menu_message(message: Message, user: UserDTO) -> None:
    bot_message = BotMessage.main_menu(user.role)
    await message.answer(**bot_message.prepare())
