from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.use_cases.get_user_info import get_user_info_use_case
from app.utils.bot_strings import bot_strings as bt

router = Router()


@router.callback_query(F.data == bt.CALLBACK_USER_INFO)
async def send_user_info(callback: CallbackQuery):
    username = callback.from_user.username
    response = await get_user_info_use_case(username)
    await callback.message.answer(response)
    await callback.answer()
