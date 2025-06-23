from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.orm import Session

from app.exceptions.teacher_exceptions import TeacherStudentsNotFound
from app.exceptions.user_exceptions import UserNotFoundException
from app.services.slot_service import SlotService
from app.services.teacher_service import TeacherService
from app.states.schedule_states import ScheduleStates

router = Router()


@router.message(ScheduleStates.new_slots_ready)
async def new_slots_ready(message: Message, state: FSMContext, session: Session):
    data = await state.get_data()
    teacher = data.get("teacher")

    teacher_service = TeacherService(session)
    try:
        teacher = teacher_service.get_teacher(teacher)
        students = teacher_service.get_unsigned_students(teacher.uuid)
    except UserNotFoundException:
        pass
    except TeacherStudentsNotFound:
        pass

    slots_service = SlotService(session)
    slots = slots_service.get_free_slots(teacher.uuid)
    message_text = await slots_service.get_slot_reply(slots)
    await message.answer(message_text)
