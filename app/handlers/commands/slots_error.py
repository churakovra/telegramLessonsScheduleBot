from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import bot_strings as bt

router = Router()


@router.message(Command("slots_error"))
async def send_slots_error(message: Message, state: FSMContext):
    await message.answer(bt.SLOTS_FAILURE_ANSWER)
    await state.set_state(ScheduleStates.wait_for_slots)
