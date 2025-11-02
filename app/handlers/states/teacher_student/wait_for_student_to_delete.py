from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.services.user_service import UserService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.message_template import MessageTemplate

router = Router()


@router.message(ScheduleStates.wait_for_student_to_delete)
async def handle_state(message: Message, session: AsyncSession, state: FSMContext):
    teacher_username = getattr(message.from_user, "username", "") or ""
    raw_msg = getattr(message, "text", "")

    student_service = StudentService(session)
    students, unknown_students = await student_service.parse_students(raw_msg)

    if len(students) <= 0:
        await message.answer(BotStrings.Teacher.TEACHER_STUDENTS_NOT_FOUND)
        await state.set_state(ScheduleStates.wait_for_student_to_delete)

    if len(unknown_students) > 0:
        if len(unknown_students) <= 1:
            message_text = BotStrings.Teacher.TEACHER_STUDENT_ADD_UNKNOWN_STUDENT
        else:
            message_text = BotStrings.Teacher.TEACHER_STUDENT_ADD_UNKNOWN_STUDENTS
        await message.answer(str.format(message_text, student=", ".join(unknown_students)))

    teacher_service = TeacherService(session)
    teacher = await teacher_service.get_teacher(teacher_username)
    await teacher_service.delete_students(students, teacher)

    await message.delete()
    user_service = UserService(session)
    user, markup = await user_service.get_user_menu(teacher_username)
    bot_message = MessageTemplate.get_menu_message(user.username, markup)
    await message.answer(
        text=bot_message.message_text, reply_markup=bot_message.reply_markup
    )
    await state.clear()
