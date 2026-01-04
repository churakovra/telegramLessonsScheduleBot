from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.notifiers.telegram_notifier import TelegramNotifier
from app.services.slot_service import SlotService
from app.services.teacher_service import TeacherService
from app.services.user_service import UserService
from app.utils.enums.bot_values import OperationType
from app.utils.exceptions.teacher_exceptions import TeacherStudentsNotFound
from app.utils.keyboards.callback_factories.slots import SendSlots
from app.utils.keyboards.markup_builder import MarkupBuilder
from app.utils.logger import setup_logger
from app.utils.message_template import MessageTemplate

router = Router()
logger = setup_logger(__name__)

@router.callback_query(SendSlots.filter())
async def handle_callback(
    callback: CallbackQuery,
    callback_data: SendSlots,
    session: AsyncSession,
    notifier: TelegramNotifier,
):
    teacher_uuid = callback_data.teacher_uuid
    teacher_service = TeacherService(session)
    slots_service = SlotService(session)

    try:
        students = await teacher_service.get_unsigned_students(teacher_uuid)
        slots = await slots_service.get_free_slots(teacher_uuid)
        markup = MarkupBuilder.days_for_students_markup(slots, teacher_uuid)
        if callback_data.operation_type == OperationType.ADD:
            message = await MessageTemplate.slots_added_for_student_message(
                slots, markup
            )
        else:
            message = await MessageTemplate.slots_updated_for_student_message(
                slots, markup
            )
        [await notifier.send_message(message, student.chat_id) for student in students]
        await callback.message.delete()
        logger.info(f"Teacher {teacher_uuid} sent slots to students")
    except TeacherStudentsNotFound as e:
        logger.error(e.message)
        await callback.message.answer(e.message)
    finally:
        user_service = UserService(session)
        user = await user_service.get_user(callback.from_user.username)
        markup = MarkupBuilder.main_menu_markup(user.role)
        bot_message = MessageTemplate.main_menu_message(user.username, markup)
        await notifier.send_message(
            bot_message=bot_message, receiver_chat_id=callback.message.chat.id
        )
        await callback.answer()
