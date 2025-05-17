from aiogram import Router
from aiogram.fsm.context import FSMContext

from app.handlers.commands.send_slots import send_slots
from app.states.schedule_states import ScheduleStates

router = Router()


@router.message(ScheduleStates.wait_slots_send_to_students)
async def wait_slots_send(state: FSMContext):
    await send_slots(state)
