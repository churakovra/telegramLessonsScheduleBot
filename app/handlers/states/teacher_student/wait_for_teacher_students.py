from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.notifiers.telegram_notifier import TelegramNotifier
from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.services.user_service import UserService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.exceptions.teacher_exceptions import TeacherAlreadyHasStudentException
from app.utils.message_template import MessageTemplate

router = Router()


@router.message(ScheduleStates.wait_for_teacher_students)
async def handle_state(
        message: Message,
        session: AsyncSession,
        state: FSMContext,
        notifier: TelegramNotifier
):
    data = await state.get_data()
    teacher_uuid = data["teacher_uuid"]
    raw_msg = message.text

    student_service = StudentService(session)
    students, unknown_students = await student_service.parse_students(raw_msg)

    if len(unknown_students) > 0:

        if len(unknown_students) <= 1:
            message_text = BotStrings.TEACHER_STUDENT_ADD_UNKNOWN_STUDENT
        else:
            message_text = BotStrings.TEACHER_STUDENT_ADD_UNKNOWN_STUDENTS
        await message.answer(str.format(message_text, ", ".join(unknown_students)))

    if len(students) > 0:
        try:
            teacher_service = TeacherService(session)
            await teacher_service.attach_students(teacher_uuid=teacher_uuid, students=students, uuid_lesson=None)
            success_students_usernames = [student.username for student in students]
        except TeacherAlreadyHasStudentException as e:
            await message.answer(e.message)
            return

        if len(success_students_usernames) <= 1:
            message_text = BotStrings.TEACHER_STUDENT_ADD_SUCCESS
        else:
            message_text = BotStrings.TEACHER_STUDENTS_ADD_SUCCESS
        await message.answer(str.format(message_text, ", ".join(success_students_usernames)))

    user_service = UserService(session)
    user, markup = await user_service.get_user_menu(message.from_user.username)
    bot_message = MessageTemplate.get_menu_message(user.username, markup)
    await notifier.send_message(
        bot_message=bot_message,
        receiver_chat_id=message.chat.id
    )
    await state.clear()
