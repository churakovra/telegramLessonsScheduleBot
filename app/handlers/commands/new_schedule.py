from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.states.schedule_states import ScheduleStates

router = Router()

roles = BotValues.UserRoles


@router.message(Command("new_schedule"))
async def set_new_schedule(message: Message, state: FSMContext):
    await message.answer(f"Привет, {message.from_user.first_name}, я жду твои окошки")
    await state.set_state(ScheduleStates.wait_for_slots)
