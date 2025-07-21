from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import UserService
from app.utils.bot_strings import bot_strings as bt
from app.utils.enums.bot_values import UserRoles
from app.utils.exceptions.user_exceptions import UserNotFoundException, UserChangeRoleException

router = Router()


@router.message(Command("make_teacher"))
async def make_teacher_from_student(message: Message, command: CommandObject, session: AsyncSession):
    # Проверяем, передали ли аргументы с командой
    if command.args is None:
        await message.answer(
            text=bt.MAKE_TEACHER_COMMAND_IS_EMPTY
        )
        return

    # Получаем username инициатора, username нового преподавателя, проверяем статусы
    initiator_user = message.from_user.username
    teacher_username = command.args.strip()

    # Меняем статус пользователю
    try:
        user_service = UserService(session)
        await user_service.add_role(initiator_user, teacher_username, UserRoles.TEACHER)
        await message.answer(bt.MAKE_TEACHER_SUCCESS.format(teacher_username))
    except (UserNotFoundException, UserChangeRoleException) as e:
        await message.answer(f"{bt.MAKE_TEACHER_FAILURE}; {e.message}")
