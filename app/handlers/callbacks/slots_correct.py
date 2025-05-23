from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.states.schedule_states import ScheduleStates
from app.use_cases.add_slots import add_slots_use_case
from app.use_cases.send_slots_to_students import send_slots_to_students_use_case
from app.utils.bot_strings import bot_strings as bt

router = Router()


@router.callback_query(F.data == bt.CALLBACK_SLOTS_CORRECT, ScheduleStates.wait_for_confirmation)
async def reply_and_save_to_db(callback: CallbackQuery, state: FSMContext, **kwargs):
    data = await state.get_data()
    slots = data.get("slots")
    notifier = kwargs["notifier"]
    teacher = callback.from_user.username

    days_from_db = await add_slots_use_case(slots)
    await send_slots_to_students_use_case(teacher, days_from_db, notifier)
    await callback.message.answer(
        text=bt.SLOTS_PROCESSING_SUCCESS_ANSWER
    )
    await callback.answer()
