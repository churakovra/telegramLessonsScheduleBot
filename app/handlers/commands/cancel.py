from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboard import fabric
from app.message.models import BotMessage
from app.schemas.user import UserDTO

router = Router()


@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext, user: UserDTO) -> None:
    await state.clear()

    markup = fabric.get_main_menu_by_role(user.role)

    # Build and send message
    bot_message = BotMessage(text="Меню", markup=markup)
    await message.answer(**bot_message.to_aiogram_kwargs())
