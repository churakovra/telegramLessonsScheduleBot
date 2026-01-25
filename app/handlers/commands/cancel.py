from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession


from app.keyboard import markup_type_by_role
from app.keyboard.builder import MarkupBuilder
from app.services.user_service import UserService
from app.utils import message_template


router = Router()


@router.message(Command("cancel"))
async def cancel(message: Message, session: AsyncSession, state: FSMContext) -> None:
    user_service = UserService(session)
    username = message.from_user.username
    user = await user_service.get_user(username)
    markup = MarkupBuilder.build(markup_type_by_role[user.role])
    reply_message = message_template.main_menu_message(markup)
    await state.clear()
    await message.answer(**reply_message)