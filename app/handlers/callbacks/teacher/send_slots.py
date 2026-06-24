from aiogram import Router
from aiogram.types import CallbackQuery

from app.keyboard.callback_factories.slot import SendSlots
from app.keyboard.fabric import days_for_students, teacher_main_menu
from app.message.models import BotMessage, MessageRecipient
from app.notifier.sender import MessageSender
from app.services.container import Services
from app.utils.bot_strings import BotStrings
from app.utils.exceptions.teacher_exceptions import TeacherStudentsNotFound
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.callback_query(SendSlots.filter())
async def handle_callback(
    callback: CallbackQuery,
    callback_data: SendSlots,
    services: Services,
    sender: MessageSender,
) -> None:
    teacher_uuid = callback_data.teacher_uuid
    try:
        students = await services.teacher.get_unsigned_students(teacher_uuid)
        slots = await services.slot.get_free_slots(teacher_uuid)

        # Build markup using fabric
        markup = days_for_students(slots=slots, teacher_uuid=teacher_uuid)

        # Build message
        message = BotMessage(text=BotStrings.Student.SLOTS_ADDED, markup=markup)

        # Send to all students via sender unified interface
        recipients = [MessageRecipient(chat_id=student.chat_id) for student in students]
        await sender.send(message=message, recipients=recipients)
        logger.info(f"Teacher {teacher_uuid} sent slots to students")
    except TeacherStudentsNotFound as e:
        logger.error(e.message)
        msg = BotMessage(text=e.message)
        await callback.message.answer(**msg.to_aiogram_kwargs())
    finally:
        markup = teacher_main_menu()
        message = BotMessage(text=BotStrings.Common.MENU, markup=markup)
        await callback.message.answer(**message.to_aiogram_kwargs())
        await callback.answer()
