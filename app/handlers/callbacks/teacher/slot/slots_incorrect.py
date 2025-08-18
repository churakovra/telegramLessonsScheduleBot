from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings

router = Router()


@router.callback_query(F.data == BotStrings.CALLBACK_SLOTS_INCORRECT)
async def retry_send_slots(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(BotStrings.SLOTS_FAILURE_ANSWER)
    await state.set_state(ScheduleStates.wait_for_slots)
    await callback.message.delete()
    await callback.answer()
