from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.notifiers.telegram_notifier import TelegramNotifier
from app.services.slot_service import SlotService
from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.services.user_service import UserService
from app.utils.bot_strings import BotStrings
from app.utils.datetime_utils import full_format_no_sec
from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.utils.keyboards.slots_for_students_markup import SlotsForStudents
from app.utils.message_template import MessageTemplate

router = Router()


@router.callback_query(SlotsForStudents.filter())
async def handle_callback(
    callback: CallbackQuery,
    callback_data: SlotsForStudents,
    session: AsyncSession,
    notifier: TelegramNotifier,
):
    slot_uuid = callback_data.uuid_slot
    student_username = callback.from_user.username

    try:
        student_service = StudentService(session)
        student = await student_service.get_student(student_username)
    except UserNotFoundException:
        raise ValueError()

    slot_service = SlotService(session)
    assigned_slot = await slot_service.assign_slot(student.uuid, slot_uuid)
    slot_time = assigned_slot.dt_start.strftime(full_format_no_sec)

    teacher_service = TeacherService(session)
    teacher = await teacher_service.get_teacher_by_uuid(assigned_slot.uuid_teacher)

    await callback.message.answer(
        BotStrings.Student.SLOTS_ASSIGN_SUCCESS_ANSWER.format(
            teacher=teacher.username,
            slot_time=slot_time,
        )
    )

    user_service = UserService(session)
    user, markup = await user_service.get_user_menu(student_username)
    bot_message = MessageTemplate.get_menu_message(user.username, markup)
    await notifier.send_message(
        bot_message=bot_message, receiver_chat_id=callback.message.chat.id
    )
    notify_teacher_message = MessageTemplate.notify_teacher_new_slot(
        student_username, slot_time
    )
    await notifier.send_message(
        bot_message=notify_teacher_message, receiver_chat_id=teacher.chat_id
    )

    await callback.message.delete()
    await callback.answer()
