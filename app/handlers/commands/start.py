from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.orm import Session

from app.handlers.commands.new_slots import UserRoles
from app.services.user_service import UserService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import bot_strings as bt

router = Router()


@router.message(Command("start"))
async def add_new_user(message: Message, state: FSMContext, session: Session):
    user_service = UserService(session)
    username = message.from_user.username
    firstname = message.from_user.first_name
    lastname = message.from_user.last_name
    chat_id = message.from_user.id
    user_service.register_user(
        username=username,
        firstname=firstname,
        lastname=lastname,
        role=UserRoles.STUDENT,
        chat_id=chat_id
    )
    await message.answer(
        text=bt.GREETING.format(firstname, username)
    )
    await state.set_state(ScheduleStates.wait_for_teacher_username)
