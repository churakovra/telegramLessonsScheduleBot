from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings

router = Router()


@router.callback_query(F.data == BotStrings.Teacher.CALLBACK_SLOTS_INCORRECT)
async def handle_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(BotStrings.Teacher.SLOTS_FAILURE)
    await state.set_state(ScheduleStates.wait_for_slots)
    await callback.message.delete()
    await callback.answer()
