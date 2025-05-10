from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.services.add_slots_to_db import add_slots
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import bot_strings as bt

router = Router()


@router.callback_query(F.data == bt.CALLBACK_SLOTS_CORRECT, ScheduleStates.wait_for_confirmation)
async def reply_and_save_to_db(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=bt.SLOTS_SUCCESS_ANSWER
    )
    data = await state.get_data()
    slots = data.get("parsed_lessons")
    await add_slots(slots)
    await callback.answer()
