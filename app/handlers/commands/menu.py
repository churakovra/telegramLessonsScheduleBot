from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.keyboard import fabric
from app.message.models import BotMessage
from app.schemas.user import UserDTO
from app.utils.logger import setup_logger

router = Router()

logger = setup_logger(__name__)


@router.message(Command("menu"))
async def send_menu_message(message: Message, user: UserDTO) -> None:
    markup = fabric.get_main_menu_by_role(user.role)

    # Build and send message
    bot_message = BotMessage(text="Меню", markup=markup)
    await message.answer(**bot_message.to_aiogram_kwargs())
