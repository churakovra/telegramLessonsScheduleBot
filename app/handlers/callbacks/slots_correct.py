from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.slot_service import SlotService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import bot_strings as bt

router = Router()


@router.callback_query(F.data == bt.CALLBACK_SLOTS_CORRECT, ScheduleStates.wait_for_confirmation)
async def reply_and_save_to_db(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    slots = data.get("slots")

    slot_service = SlotService(session)
    await slot_service.add_slots(slots)
    await callback.message.answer(
        text=bt.SLOTS_PROCESSING_SUCCESS_ANSWER
    )
    await callback.answer()
    await state.set_state(ScheduleStates.new_slots_ready)
