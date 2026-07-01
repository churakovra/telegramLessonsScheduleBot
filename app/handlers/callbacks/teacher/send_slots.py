from uuid import UUID

from aiogram import Router
from aiogram.types import CallbackQuery

from app.keyboard.callback_factories.slot import SendSlots, SendTeacherSlots
from app.keyboard.fabric import days_for_students, teacher_main_menu
from app.message.models import BotMessage, MessageRecipient
from app.notifier.sender import MessageSender
from app.services.container import Services
from app.utils.bot_strings import BotStrings
from app.utils.exceptions.teacher_exceptions import TeacherStudentsNotFound
from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


async def _send_slots_to_students(
    *,
    callback: CallbackQuery,
    teacher_uuid: UUID,
    services: Services,
    sender: MessageSender,
) -> None:
    try:
        students = await services.teacher.get_unsigned_students(teacher_uuid)
    except TeacherStudentsNotFound as e:
        logger.info(e.message)
        students = []

    slots = await services.slot.get_free_slots(teacher_uuid)
    markup = days_for_students(slots=slots, teacher_uuid=teacher_uuid)
    message = BotMessage(text=BotStrings.Student.SLOTS_ADDED, markup=markup)

    recipients = [MessageRecipient(chat_id=student.chat_id) for student in students]
    if recipients:
        await sender.send(message=message, recipients=recipients)
    logger.info(f"Teacher {teacher_uuid} sent slots to {len(recipients)} students")

    markup = teacher_main_menu()
    msg = BotMessage(
        text=BotStrings.Teacher.SLOTS_SENT.format(count=len(recipients)),
        markup=markup,
    )
    await callback.message.answer(**msg.to_aiogram_kwargs())


@router.callback_query(SendSlots.filter())
async def handle_callback(
    callback: CallbackQuery,
    callback_data: SendSlots,
    services: Services,
    sender: MessageSender,
) -> None:
    try:
        await _send_slots_to_students(
            callback=callback,
            teacher_uuid=callback_data.teacher_uuid,
            services=services,
            sender=sender,
        )
    finally:
        await callback.answer()


@router.callback_query(SendTeacherSlots.filter())
async def handle_teacher_send_slots(
    callback: CallbackQuery,
    services: Services,
    sender: MessageSender,
) -> None:
    try:
        teacher = await services.teacher.get_teacher(callback.from_user.username)
        await _send_slots_to_students(
            callback=callback,
            teacher_uuid=teacher.uuid,
            services=services,
            sender=sender,
        )
    except UserNotFoundException as e:
        logger.error(e.message)
        msg = BotMessage(text=BotStrings.Common.NOT_ENOUGH_RIGHTS)
        await callback.message.answer(**msg.to_aiogram_kwargs())
    finally:
        await callback.answer()
