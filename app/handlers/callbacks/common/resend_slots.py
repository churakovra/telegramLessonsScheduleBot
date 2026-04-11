from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboard.callback_factories.slot import ResendSlotsCallback
from app.keyboard.fabric import days_for_students
from app.message.models import BotMessage, MarkupData
from app.message.utils import slots_to_reply
from app.services.slot_service import SlotService
from app.utils.bot_strings import BotStrings

router = Router()


@router.callback_query(ResendSlotsCallback.filter())
async def handle_callback(
    callback: CallbackQuery,
    callback_data: ResendSlotsCallback,
    session: AsyncSession,
) -> None:
    slots_service = SlotService(session)
    slots = await slots_service.get_free_slots(callback_data.teacher_uuid)
    
    # Build markup using fabric
    markup = days_for_students(
        type("Context", (), {
            "teacher_uuid": callback_data.teacher_uuid,
            "slots": slots
        })()
    )
    
    # Build message
    message = BotMessage(text=BotStrings.Student.SLOTS_ADDED, markup=markup)
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()
