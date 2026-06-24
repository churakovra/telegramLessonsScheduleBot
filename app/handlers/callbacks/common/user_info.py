from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.message.models import BotMessage
from app.services.container import Services
from app.utils.bot_strings import BotStrings

router = Router()


@router.callback_query(F.data == BotStrings.User.CALLBACK_USER_INFO)
async def send_user_info(callback: CallbackQuery, services: Services):
    username = getattr(callback.from_user, "username", "") or ""
    response = await services.user.get_user_info(username)
    if callback.message:
        message = BotMessage(text=response)
        await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()
