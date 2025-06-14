from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.exceptions.user_exceptions import UserStatusError
from app.states.schedule_states import ScheduleStates
from app.use_cases.check_user_status import check_user_status_use_case
from app.utils.bot_strings import bot_strings as bt
from app.utils.bot_values import BotValues

router = Router()

UserRoles = BotValues.UserRoles


@router.message(Command("new_slots"))
async def set_new_slots(message: Message, state: FSMContext):
    try:
        await check_user_status_use_case(message.from_user.username, UserRoles.TEACHER)
    except UserStatusError:
        await message.answer(bt.SLOTS_NOT_ENOUGH_RIGHTS)
        return

    await message.answer(f"Привет, {message.from_user.first_name}, я жду твои окошки")
    await state.set_state(ScheduleStates.wait_for_slots)
