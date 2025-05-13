from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.handlers.commands.my_info import get_my_info
from app.utils.bot_strings import bot_strings as bt
from app.utils.get_user_info import get_user_info

router = Router()


@router.callback_query(F.data == bt.CALLBACK_USER_INFO)
async def send_user_info(callback: CallbackQuery):
    username = callback.from_user.username
    response = await get_user_info(username)
    await callback.message.answer(response)
    await callback.answer()
