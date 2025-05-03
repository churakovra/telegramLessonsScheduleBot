from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.handlers.commands.slots_error import send_slots_error
from app.utils.bot_strings import bot_strings as bt

router = Router()


@router.callback_query(F.data == bt.CALLBACK_SLOTS_INCORRECT)
async def retry_send_slots(callback: CallbackQuery, state: FSMContext):
    await send_slots_error(callback.message, state)
    await callback.answer()
