from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.keyboard import fabric
from app.message.models import BotMessage
from app.schemas.user import UserDTO
from app.services.container import Services
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import UserRole
from app.utils.logger import setup_logger

router = Router()

logger = setup_logger(__name__)


@router.message(Command("menu"))
async def send_menu_message(message: Message, user: UserDTO, services: Services) -> None:
    if user.role == UserRole.TEACHER:
        pending_count = await services.join_request.count_pending_for_teacher(user.uuid)
        markup = fabric.teacher_main_menu(pending_join_requests_count=pending_count)
    else:
        markup = fabric.get_main_menu_by_role(user.role)

    # Build and send message
    bot_message = BotMessage(text=BotStrings.Menu.MENU, markup=markup)
    await message.answer(**bot_message.to_aiogram_kwargs())
