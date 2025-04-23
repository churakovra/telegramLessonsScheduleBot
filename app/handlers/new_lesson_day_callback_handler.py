from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.utils.bot_strings import BotStrings

new_lesson_day_callback = Router()


@new_lesson_day_callback.callback_query(F.data == BotStrings.CALLBACK_BRANCH_DAYS)
async def reply_available_days(callback: CallbackQuery):
    await callback.message.answer(
        text=BotStrings.WEEKDAY
    )
    await callback.answer()
