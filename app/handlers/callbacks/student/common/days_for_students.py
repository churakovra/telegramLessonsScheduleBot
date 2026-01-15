from datetime import datetime

from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.slot_service import SlotService
from app.utils.datetime_utils import day_format
from app.utils.enums.bot_values import KeyboardType
from app.utils.exceptions.slot_exceptions import SlotFreeNotFoundException
from app.keyboard.callback_factories.slots import DaysForStudents
from app.keyboard.builder import MarkupBuilder
from app.keyboard.context import SlotsForStudentsKeyboardContext

router = Router()


@router.callback_query(DaysForStudents.filter())
async def handle_callback(
    callback: CallbackQuery, callback_data: DaysForStudents, session: AsyncSession
):
    day = datetime.strptime(callback_data.day, day_format)
    teacher_uuid = callback_data.teacher_uuid
    try:
        slot_service = SlotService(session)
        slots = await slot_service.get_day_slots(day, teacher_uuid)
        markup_context = SlotsForStudentsKeyboardContext(teacher_uuid, slots)
        markup = MarkupBuilder.build(KeyboardType.SLOTS_FOR_STUDENTS, markup_context)
        await callback.message.answer(text=callback.message.text, reply_markup=markup)
        await callback.message.delete()
    except SlotFreeNotFoundException as e:
        await callback.message.answer(str(e))
    finally:
        await callback.answer()
