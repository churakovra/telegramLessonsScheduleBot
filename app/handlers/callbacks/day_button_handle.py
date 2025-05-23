from aiogram import Router
from aiogram.types import CallbackQuery

from app.keyboards.days_for_students_markup import DaysForStudents
from app.use_cases.get_slots_markup import get_slots_markup_use_case

router = Router()


@router.callback_query(DaysForStudents.filter())
async def handle_day_callback(
        callback: CallbackQuery,
        callback_data: DaysForStudents
):
    uuid_day = callback_data.day_uuid
    markup = await get_slots_markup_use_case(uuid_day)
    await callback.message.edit_reply_markup(reply_markup=markup)
    await callback.answer()
