from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.orm import Session

from app.exceptions.user_exceptions import UserNotFoundException
from app.services.teacher_service import TeacherService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import bot_strings as bt

router = Router()


@router.message(Command("new_slots"))
async def set_new_slots(message: Message, state: FSMContext, session: Session):
    teacher_service = TeacherService(session)
    try:
        teacher_service.get_teacher(message.from_user.username)
    except UserNotFoundException:
        await message.answer(bt.SLOTS_NOT_ENOUGH_RIGHTS)
        return

    await message.answer(f"Привет, {message.from_user.first_name}, я жду твои окошки")
    await state.set_state(ScheduleStates.wait_for_slots)
