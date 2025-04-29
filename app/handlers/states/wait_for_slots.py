from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.states.schedule_states import ScheduleStates
from app.utils.parse_slots import parse_slots

router = Router()


@router.message(ScheduleStates.wait_for_slots)
async def wait_for_slots(message: Message, state: FSMContext):
    slots_raw = message.text
    await message.answer("Получил, обрабатываю")
    parsed_lessons = parse_slots(slots_raw, message.from_user.username)
    await message.answer("Обработал!")
    await state.clear()
