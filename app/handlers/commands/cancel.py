from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.message.message import BotMessage
from app.schemas.user import UserDTO

router = Router()


@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext, user: UserDTO) -> None:
    await state.clear()
    bot_message = BotMessage.main_menu(user.role)
    await message.answer(**bot_message.prepare())
