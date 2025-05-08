from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from app.utils.bot_strings import bot_strings as bt
from app.utils.bot_values import BotValues
from app.utils.check_user_status import check_user_status
from app.utils.change_user_status import change_user_status

router = Router()

roles = BotValues.UserRoles

@router.message(Command("make_teacher"))
async def make_teacher_from_student(message: Message, command: CommandObject):
    # Проверяем, передали ли аргументы с командой
    if command.args is None:
        await message.answer(
            text=bt.MAKE_TEACHER_COMMAND_IS_EMPTY
        )
        return

    # Получаем юзернейм того, кто хочет перевести в преподы, юзернейм потенциального препода, проверяем статусы
    initiator_user = message.from_user.username
    teacher_username = command.args.strip()
    user_is_admin = await check_user_status(initiator_user, roles.ADMIN)
    teacher_is_student = await check_user_status(teacher_username, roles.STUDENT)
    # Если статусы кривые, закругляемся
    if not user_is_admin or not teacher_is_student:
        await message.answer(bt.MAKE_TEACHER_STATUS_ERROR)
        return

    # Меняем статус пользователю
    teacher_maked = await change_user_status(initiator_user, teacher_username, roles.TEACHER)

    if teacher_maked:
        await message.answer(bt.MAKE_TEACHER_SUCCESS)
    else:
        await message.answer(bt.MAKE_TEACHER_FAILURE)
