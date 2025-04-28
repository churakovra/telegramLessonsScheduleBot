import asyncio

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.states.schedule_states import ScheduleStates

router = Router()


@router.message(ScheduleStates.wait_for_slots)
async def wait_for_slots(message: Message, state: FSMContext):
    slots_raw = message.text
    print(slots_raw)
    await message.answer("Получил, обрабатываю")
    await asyncio.sleep(3)
    await message.answer("Обработал!")
    await state.clear()
