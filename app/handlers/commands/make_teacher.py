from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import UserService
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import UserRole
from app.utils.exceptions.user_exceptions import UserNotFoundException, UserChangeRoleException

router = Router()


@router.message(Command("make_teacher"))
async def make_teacher_from_student(message: Message, command: CommandObject, session: AsyncSession):
    # check if command has args
    if command.args is None:
        await message.answer(
            text=BotStrings.Admin.MAKE_TEACHER_COMMAND_IS_EMPTY
        )
        return

    # Get initiator username, new teacher username, check statuses
    initiator_user = getattr(message.from_user, "username", "") or ""
    teacher_username = command.args.strip()

    # Add role to new teacher
    try:
        user_service = UserService(session)
        await user_service.add_role(initiator_user, teacher_username, UserRole.TEACHER)
        await message.answer(BotStrings.Admin.MAKE_TEACHER_SUCCESS.format(teacher_username))
    except (UserNotFoundException, UserChangeRoleException) as e:
        await message.answer(f"{BotStrings.Admin.MAKE_TEACHER_FAILURE}; {e.message}")
