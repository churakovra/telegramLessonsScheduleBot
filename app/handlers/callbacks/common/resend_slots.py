from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.notifiers.telegram_notifier import TelegramNotifier
from app.services.slot_service import SlotService
from app.utils.keyboards.callback_factories.slots import ResendSlots
from app.utils.keyboards.markup_builder import MarkupBuilder
from app.utils.message_template import MessageTemplate

router = Router()


@router.callback_query(ResendSlots.filter())
async def handle_callback(
    callback: CallbackQuery,
    callback_data: ResendSlots,
    session: AsyncSession,
    notifier: TelegramNotifier,
):
    slots_service = SlotService(session)
    slots = await slots_service.get_free_slots(callback_data.teacher_uuid)
    markup = MarkupBuilder.days_for_students_markup(slots, callback_data.teacher_uuid)
    message = await MessageTemplate.slots_added_for_student_message(slots, markup)
    await notifier.send_message(message, callback_data.student_chat_id)
