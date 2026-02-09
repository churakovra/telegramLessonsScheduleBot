from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboard import markup_type_by_role
from app.keyboard.builder import MarkupBuilder
from app.schemas.user_dto import UserDTO
from app.utils import message_template


router = Router()


@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext, user: UserDTO) -> None:
    markup = MarkupBuilder.build(markup_type_by_role[user.role])
    reply_message = message_template.main_menu_message(markup)
    await state.clear()
    await message.answer(**reply_message)
