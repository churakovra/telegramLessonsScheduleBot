from aiogram import Router
from aiogram.types import CallbackQuery

from app.keyboard.callback_factories.slot import ResendSlotsCallback
from app.keyboard.fabric import days_for_students
from app.message.models import BotMessage
from app.services.container import Services
from app.utils.bot_strings import BotStrings

router = Router()


@router.callback_query(ResendSlotsCallback.filter())
async def handle_callback(
    callback: CallbackQuery,
    callback_data: ResendSlotsCallback,
    services: Services,
) -> None:
    slots = await services.slot.get_free_slots(callback_data.teacher_uuid)

    # Build markup using fabric
    markup = days_for_students(slots=slots, teacher_uuid=callback_data.teacher_uuid)

    # Build message
    message = BotMessage(text=BotStrings.Student.SLOTS_ADDED, markup=markup)
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()
