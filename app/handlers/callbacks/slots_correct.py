from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.utils.bot_strings import bot_strings as bt

router = Router()


@router.callback_query(F.data == bt.CALLBACK_SLOTS_CORRECT)
async def reply_and_save_to_db(callback: CallbackQuery):
    await callback.message.answer(
        text=bt.SLOTS_SUCCESS_ANSWER
    )
    await callback.answer()
