from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboard import fabric
from app.message.models import BotMessage
from app.schemas.user import UserDTO
from app.utils.enums.bot_values import UserRole

router = Router()


@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext, user: UserDTO) -> None:
    await state.clear()

    # Get markup based on role
    if user.role == UserRole.TEACHER:
        markup = fabric.teacher_main_menu()
    elif user.role == UserRole.STUDENT:
        markup = fabric.student_main_menu()
    elif user.role == UserRole.ADMIN:
        markup = fabric.admin_main_menu()
    else:
        markup = None

    # Build and send message
    bot_message = BotMessage(text="Меню", markup=markup)
    await message.answer(**bot_message.to_aiogram_kwargs())
