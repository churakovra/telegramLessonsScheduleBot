from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.states.schedule_states import ScheduleStates
from app.use_cases.attach_student_to_teacher import attach_student_to_teacher_use_case

router = Router()


@router.message(ScheduleStates.wait_for_teacher_username)
async def process_teacher_username(message: Message, state: FSMContext):
    student_username = message.from_user.username
    teacher_username = message.text

    if await attach_student_to_teacher_use_case(teacher_username, student_username):
        await message.answer("Ура! Победа! ZZZZZZ")
        await state.clear()
    else:
        await message.answer("Попробуйте еще раз")
        await state.set_state(ScheduleStates.wait_for_teacher_username)
