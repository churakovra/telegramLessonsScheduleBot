from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.models.user_dto import UserDTO
from app.states.schedule_states import ScheduleStates
from app.use_cases.register_new_user import register_new_user_use_case
from app.utils.bot_strings import bot_strings as bt

router = Router()


@router.message(Command("start"))
async def add_new_user(message: Message, state: FSMContext):
    student_username = message.from_user.username
    student_firstname = message.from_user.first_name
    student_lastname = message.from_user.last_name
    student_chat_id = message.from_user.id

    user = UserDTO.register_user(
        username=student_username,
        firstname=student_firstname,
        lastname=student_lastname,
        chat_id=student_chat_id
    )
    await register_new_user_use_case(user)

    await message.answer(
        text=bt.GREETING.format(student_firstname, student_username)
    )
    await state.set_state(ScheduleStates.wait_for_teacher_username)
