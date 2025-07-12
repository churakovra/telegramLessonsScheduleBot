from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.states.schedule_states import ScheduleStates

router = Router()


@router.message(ScheduleStates.wait_for_teacher_username)
async def process_teacher_username(
        message: Message,
        state: FSMContext,
        session: AsyncSession
):
    teacher_username = message.text
    student_username = message.from_user.username

    teacher_service = TeacherService(session)
    student_service = StudentService(session)
    try:
        teacher = await teacher_service.get_teacher(teacher_username)
        student = await student_service.get_student(student_username)
        await teacher_service.attach_student(teacher_uuid=teacher.uuid, student_uuid=student.uuid)
        await state.clear()
    except Exception:
        await message.answer("Попробуйте еще раз")
        await state.set_state(ScheduleStates.wait_for_teacher_username)
