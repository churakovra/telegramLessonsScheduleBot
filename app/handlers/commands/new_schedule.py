from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import bot_strings as bt
from app.utils.bot_values import BotValues
from app.utils.check_user_status import check_user_status

router = Router()

roles = BotValues.UserRoles


@router.message(Command("new_schedule"))
async def set_new_schedule(message: Message, state: FSMContext):
    is_user_teacher = await check_user_status(message.from_user.username, roles.TEACHER)

    if not is_user_teacher:
        await message.answer(bt.SLOTS_NOT_ENOUGH_RIGHTS)
        return

    await message.answer(f"Привет, {message.from_user.first_name}, я жду твои окошки")
    await state.set_state(ScheduleStates.wait_for_slots)
