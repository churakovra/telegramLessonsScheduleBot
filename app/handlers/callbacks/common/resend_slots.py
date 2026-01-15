from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.notifiers.telegram_notifier import TelegramNotifier
from app.services.slot_service import SlotService
from app.utils.enums.bot_values import KeyboardType
from app.keyboard.callback_factories.slots import ResendSlots
from app.keyboard.builder import MarkupBuilder
from app.keyboard.context import DaysForStudentsKeyboardContext
from app.utils.message_template import slots_added_for_student_message

router = Router()


@router.callback_query(ResendSlots.filter())
async def handle_callback(
    callback: CallbackQuery,
    callback_data: ResendSlots,
    session: AsyncSession,
    notifier: TelegramNotifier,
) -> None:
    slots_service = SlotService(session)
    slots = await slots_service.get_free_slots(callback_data.teacher_uuid)
    markup_context = DaysForStudentsKeyboardContext(callback_data.teacher_uuid, slots)
    markup = MarkupBuilder.build(KeyboardType.DAYS_FOR_STUDENTS, markup_context)
    reply = await slots_service.get_parsed_slots_reply(slots)
    message = slots_added_for_student_message(reply, markup)
    await notifier.send_message(message, callback_data.student_chat_id)
