from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from app.use_cases.make_teacher import make_teacher_use_case
from app.utils.bot_strings import bot_strings as bt
from app.utils.bot_values import BotValues

router = Router()

UserRoles = BotValues.UserRoles


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

    # Меняем статус пользователю
    teacher_maked = await make_teacher_use_case(initiator_user, teacher_username)

    if teacher_maked:
        await message.answer(bt.MAKE_TEACHER_SUCCESS)
    else:
        await message.answer(bt.MAKE_TEACHER_FAILURE)
