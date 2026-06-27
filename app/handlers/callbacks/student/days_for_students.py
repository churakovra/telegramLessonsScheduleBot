from datetime import datetime

from aiogram import Router
from aiogram.types import CallbackQuery

from app.keyboard.callback_factories.slot import DaysForStudents
from app.keyboard.fabric import slots_for_students
from app.message.models import BotMessage
from app.services.container import Services
from app.utils.datetime_utils import day_format
from app.utils.exceptions.slot_exceptions import SlotFreeNotFoundException

router = Router()


@router.callback_query(DaysForStudents.filter())
async def handle_callback(
    callback: CallbackQuery, callback_data: DaysForStudents, services: Services
):
    day = datetime.strptime(callback_data.day, day_format)
    teacher_uuid = callback_data.teacher_uuid
    try:
        slots = await services.slot.get_day_slots(day, teacher_uuid)

        # Build markup using fabric
        markup = slots_for_students(slots=slots)

        # Build message
        text = callback.message.text or "Выберите время"
        message = BotMessage(text=text, markup=markup)
        await callback.message.answer(**message.to_aiogram_kwargs())
        await callback.message.delete()
    except SlotFreeNotFoundException as e:
        message = BotMessage(text=str(e))
        await callback.message.answer(**message.to_aiogram_kwargs())
    finally:
        await callback.answer()
