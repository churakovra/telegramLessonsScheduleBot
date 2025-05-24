from aiogram import Router
from aiogram.types import CallbackQuery

from app.keyboards.slots_for_students_markup import SlotsForStudents
from app.use_cases.assign_slot import assign_slot_use_case
from app.use_cases.get_slot import get_slot_use_case

from app.utils.bot_strings import bot_strings as bt
from app.utils.datetime_utils import full_format_no_sec

router = Router()


@router.callback_query(SlotsForStudents.filter())
async def slot_button_handle(
        callback: CallbackQuery,
        callback_data: SlotsForStudents
):
    uuid_slot = callback_data.uuid_slot
    slot = await get_slot_use_case(uuid_slot)
    student = callback.from_user.username
    await assign_slot_use_case(slot, student)
    await callback.message.answer(bt.SLOTS_ASSIGN_SUCCESS_ANSWER.format(slot.t_username, slot.dt_start.strftime(full_format_no_sec)))
    await callback.answer()
