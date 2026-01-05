from datetime import datetime

from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.slot_service import SlotService
from app.utils.datetime_utils import day_format
from app.utils.exceptions.slot_exceptions import SlotFreeNotFoundException
from app.utils.keyboards.callback_factories.slots import DaysForStudents
from app.utils.keyboards.markup_builder import MarkupBuilder

router = Router()


@router.callback_query(DaysForStudents.filter())
async def handle_callback(
        callback: CallbackQuery,
        callback_data: DaysForStudents,
        session: AsyncSession
):
    day = datetime.strptime(callback_data.day, day_format)
    teacher_uuid = callback_data.teacher_uuid

    try:
        slot_service = SlotService(session)
        slots = await slot_service.get_day_slots(day, teacher_uuid)
        markup = MarkupBuilder.slots_for_students_markup(slots, teacher_uuid)
        await callback.message.answer(
            text=callback.message.text,
            reply_markup=markup
        )

        await callback.message.delete()

    except SlotFreeNotFoundException as e:
        await callback.message.answer(str(e))
    finally:
        await callback.answer()
