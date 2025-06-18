from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.states.schedule_states import ScheduleStates
from app.use_cases.register_user import RegisterUserUseCase
from app.utils.bot_strings import bot_strings as bt

router = Router()


@router.message(Command("start"))
async def add_new_user(message: Message, state: FSMContext, session: AsyncSession):
    use_case = RegisterUserUseCase(session)
    use_case.register_user(
        username=message.from_user.username,
        firstname=message.from_user.first_name,
        lastname=message.from_user.last_name,
        chat_id=message.from_user.id
    )
    await message.answer(text=bt.GREETING.format(message.from_user.first_name, message.from_user.username))
    await state.set_state(ScheduleStates.wait_for_teacher_username)
