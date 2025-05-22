from aiogram import Router
from aiogram.types import CallbackQuery

from app.keyboards.days_for_students_markup import DaysForStudents
from app.keyboards.slots_for_students_markup import get_slots_for_students_markup

router = Router()


@router.callback_query(DaysForStudents.filter())
async def handle_day_callback(
        callback: CallbackQuery,
        callback_data: DaysForStudents
):
    await callback.message.answer("pipikaka")
    day_uuid = callback_data.day_uuid
    markup = await get_slots_for_students_markup(day_uuid)
    await callback.message.edit_reply_markup(reply_markup=markup)
    await callback.answer()
