from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.repositories.slots_repo import SlotsRepo
from app.states.schedule_states import ScheduleStates
from app.use_cases.add_slots import add_slots_use_case
from app.utils.bot_strings import bot_strings as bt

router = Router()


@router.callback_query(F.data == bt.CALLBACK_SLOTS_CORRECT, ScheduleStates.wait_for_confirmation)
async def reply_and_save_to_db(callback: CallbackQuery, state: FSMContext, **kwargs):
    data = await state.get_data()
    slots = data.get("slots")
    notifier = kwargs["notifier"]

    await add_slots_use_case(slots)

    await state.set_state(ScheduleStates.wait_slots_send_to_students)
    await state.update_data(slots=slots)
    await callback.answer()
