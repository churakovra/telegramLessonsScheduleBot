from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.notifiers.telegram_notifier import TelegramNotifier
from app.services.slot_service import SlotService
from app.services.teacher_service import TeacherService
from app.services.user_service import UserService
from app.utils.enums.bot_values import KeyboardType, OperationType
from app.utils.exceptions.teacher_exceptions import TeacherStudentsNotFound
from app.utils.keyboard import markup_type_by_role
from app.utils.keyboard.builder import MarkupBuilder
from app.utils.keyboard.callback_factories.slots import SendSlots
from app.utils.keyboard.context import DaysForStudentsKeyboardContext
from app.utils.logger import setup_logger
from app.utils.message_template import (
    main_menu_message,
    slots_added_for_student_message,
    slots_updated_for_student_message,
)

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
        makrup_context = DaysForStudentsKeyboardContext(slots, teacher_uuid)
        markup = MarkupBuilder.build(KeyboardType.DAYS_FOR_STUDENTS, makrup_context)
        if callback_data.operation_type == OperationType.ADD:
            message = await slots_added_for_student_message(slots, markup)
        else:
            message = await slots_updated_for_student_message(slots, markup)
        [await notifier.send_message(message, student.chat_id) for student in students]
        await callback.message.delete()
        logger.info(f"Teacher {teacher_uuid} sent slots to students")
    except TeacherStudentsNotFound as e:
        logger.error(e.message)
        await callback.message.answer(e.message)
    finally:
        user_service = UserService(session)
        user = await user_service.get_user(callback.from_user.username)
        markup = MarkupBuilder.build(markup_type_by_role[user.role])
        bot_message = main_menu_message(user.username, markup)
        await notifier.send_message(
            bot_message=bot_message, receiver_chat_id=callback.message.chat.id
        )
        await callback.answer()
