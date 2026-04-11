from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboard.callback_factories.slot import SendSlots
from app.keyboard.fabric import days_for_students, teacher_main_menu
from app.message.models import BotMessage, MessageEnvelope, MessageRecipient
from app.notifier.producer import MessageProducer
from app.services.slot_service import SlotService
from app.services.teacher_service import TeacherService
from app.utils.bot_strings import BotStrings
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
    try:
        students = await teacher_service.get_unsigned_students(teacher_uuid)
        slots = await slots_service.get_free_slots(teacher_uuid)
        
        # Build markup using fabric
        markup = days_for_students(
            type("Context", (), {
                "teacher_uuid": teacher_uuid,
                "slots": slots
            })()
        )
        
        # Build message
        message = BotMessage(text=BotStrings.Student.SLOTS_ADDED, markup=markup)
        
        # Create envelope with recipients
        envelope = MessageEnvelope(
            message=message,
            recipients=[MessageRecipient(chat_id=student.chat_id) for student in students]
        )
        
        await producer.produce(envelope)
        logger.info(f"Teacher {teacher_uuid} sent slots to students")
    except TeacherStudentsNotFound as e:
        logger.error(e.message)
        await callback.message.answer(e.message)
    finally:
        markup = teacher_main_menu()
        message = BotMessage(text=BotStrings.Common.MENU, markup=markup)
        await callback.message.answer(**message.to_aiogram_kwargs())
        await callback.answer()
