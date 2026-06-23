from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from app.message.models import BotMessage
from app.services.container import Services
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import UserRole
from app.utils.exceptions.user_exceptions import (
    UserChangeRoleException,
    UserNotFoundException,
)
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.message(Command("make_teacher"))
async def make_teacher_from_student(
    message: Message, command: CommandObject, services: Services
):
    if not command.args:
        msg = BotMessage(text=BotStrings.Admin.MAKE_TEACHER_COMMAND_IS_EMPTY)
        await message.answer(**msg.to_aiogram_kwargs())
        return
    initiator_user = message.from_user.username
    teacher_username = command.args.strip()
    try:
        await services.user.add_role(initiator_user, teacher_username, UserRole.TEACHER)
        msg = BotMessage(
            text=BotStrings.Admin.MAKE_TEACHER_SUCCESS.format(user=teacher_username)
        )
        await message.answer(**msg.to_aiogram_kwargs())
        logger.info(
            f"User {teacher_username} having {UserRole.TEACHER} now. Initiator is {initiator_user}"
        )
    except (UserNotFoundException, UserChangeRoleException) as e:
        logger.error(e.message)
        msg = BotMessage(text=f"{BotStrings.Admin.MAKE_TEACHER_FAILURE}; {e.message}")
        await message.answer(**msg.to_aiogram_kwargs())
