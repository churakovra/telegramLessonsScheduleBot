from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboard.callback_factories.slot import SendSlots
from app.message import context
from app.message.message import BotMessage
from app.message.message_pack import MessagePack, MessageRecipient
from app.notifier.producer import MessageProducer
from app.services.slot_service import SlotService
from app.services.teacher_service import TeacherService
from app.utils.enums.bot_values import UserRole
from app.utils.exceptions.teacher_exceptions import TeacherStudentsNotFound
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.callback_query(SendSlots.filter())
async def handle_callback(
    callback: CallbackQuery,
    callback_data: SendSlots,
    session: AsyncSession,
    producer: MessageProducer,
):
    teacher_uuid = callback_data.teacher_uuid
    teacher_service = TeacherService(session)
    slots_service = SlotService(session)
    message_context: context.AbstractBotMessageContext
    try:
        students = await teacher_service.get_unsigned_students(teacher_uuid)
        slots = await slots_service.get_free_slots(teacher_uuid)
        message_context = context.DaysForStudents(teacher_uuid, slots)
        message_pack = MessagePack(
            message_context=message_context,
            message_recipients=[
                MessageRecipient(chat_id=student.chat_id) for student in students
            ],
        )
        await producer.produce(message_pack)
        logger.info(f"Teacher {teacher_uuid} sent slots to students")
    except TeacherStudentsNotFound as e:
        logger.error(e.message)
        await callback.message.answer(e.message)
    finally:
        message = BotMessage.main_menu(UserRole.TEACHER)
        await callback.message.answer(**message.prepare())
        await callback.answer()
