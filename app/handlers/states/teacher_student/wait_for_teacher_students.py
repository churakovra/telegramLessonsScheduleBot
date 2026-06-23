from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboard import fabric
from app.message.models import BotMessage
from app.services.container import Services
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.exceptions.teacher_exceptions import TeacherAlreadyHasStudentException

router = Router()


@router.message(ScheduleStates.wait_for_teacher_students)
async def handle_state(
    message: Message,
    services: Services,
    state: FSMContext,
):
    data = await state.get_data()
    teacher_uuid = data["teacher_uuid"]
    raw_msg = message.text

    students, unknown_students = await services.student.parse_students(raw_msg)

    if len(unknown_students) > 0:
        if len(unknown_students) <= 1:
            message_text = BotStrings.Teacher.TEACHER_STUDENT_ADD_UNKNOWN_STUDENT
        else:
            message_text = BotStrings.Teacher.TEACHER_STUDENT_ADD_UNKNOWN_STUDENTS
        msg = BotMessage(
            text=str.format(message_text, student=", ".join(unknown_students))
        )
        await message.answer(**msg.to_aiogram_kwargs())

    if len(students) > 0:
        try:
            await services.teacher.attach_students(
                teacher_uuid=teacher_uuid, students=students, uuid_lesson=None
            )
            success_students_usernames = [student.username for student in students]
        except TeacherAlreadyHasStudentException as e:
            msg = BotMessage(text=e.message)
            await message.answer(**msg.to_aiogram_kwargs())
            return

        if len(success_students_usernames) <= 1:
            message_text = BotStrings.Teacher.TEACHER_STUDENT_ADD_SUCCESS
        else:
            message_text = BotStrings.Teacher.TEACHER_STUDENTS_ADD_SUCCESS
        msg = BotMessage(
            text=str.format(message_text, student=", ".join(success_students_usernames))
        )
        await message.answer(**msg.to_aiogram_kwargs())

    await state.clear()

    msg = BotMessage(text=BotStrings.Common.MENU, markup=fabric.teacher_main_menu())
    await message.answer(**msg.to_aiogram_kwargs())
