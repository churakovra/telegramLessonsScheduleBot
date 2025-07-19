from aiogram import Router
from aiogram.types import CallbackQuery

from app.utils.keyboards.days_for_students_markup import DaysForStudents
from app.utils.keyboards.slots_for_students_markup import get_slots_for_students_markup

router = Router()


@router.callback_query(DaysForStudents.filter())
async def handle_day_callback(
        callback: CallbackQuery,
        callback_data: DaysForStudents
):
    slots = callback_data.slots
    teacher_uuid = callback_data.teacher_uuid
    markup = get_slots_for_students_markup(slots, teacher_uuid)
    await callback.message.edit_reply_markup(reply_markup=markup)
    await callback.answer()
