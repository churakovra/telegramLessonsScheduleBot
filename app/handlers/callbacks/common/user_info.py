from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.message.models import BotMessage
from app.services.user_service import UserService
from app.utils.bot_strings import BotStrings

router = Router()


@router.callback_query(F.data == BotStrings.User.CALLBACK_USER_INFO)
async def send_user_info(callback: CallbackQuery, session: AsyncSession):
    username = getattr(callback.from_user, "username", "") or ""
    user_service = UserService(session)
    response = await user_service.get_user_info(username)
    if callback.message:
        message = BotMessage(text=response)
        await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()
