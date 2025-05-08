from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.handlers.commands.make_slots import make_slots
from app.states.schedule_states import ScheduleStates

router = Router()


@router.message(ScheduleStates.wait_for_slots)
async def wait_for_slots(message: Message, state: FSMContext):
    await make_slots(message, state)
