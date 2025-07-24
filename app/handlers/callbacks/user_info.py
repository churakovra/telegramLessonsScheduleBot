from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import UserService
from app.utils.bot_strings import BotStrings

router = Router()


@router.callback_query(F.data == BotStrings.CALLBACK_USER_INFO)
async def send_user_info(callback: CallbackQuery, session: AsyncSession):
    username = callback.from_user.username
    user_service = UserService(session)
    response = await user_service.get_user_info(username)

    await callback.message.answer(response)
    await callback.answer()
