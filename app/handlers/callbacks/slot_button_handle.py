from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.utils.keyboards.slots_for_students_markup import SlotsForStudents
from app.services.slot_service import SlotService
from app.services.student_service import StudentService
from app.utils.bot_strings import bot_strings as bt
from app.utils.datetime_utils import full_format_no_sec

router = Router()


@router.callback_query(SlotsForStudents.filter())
async def slot_button_handle(
        callback: CallbackQuery,
        callback_data: SlotsForStudents,
        session: AsyncSession
):
    slot_uuid = callback_data.uuid_slot

    student_service = StudentService(session)
    student_username = callback.from_user.username
    try:
        student = await student_service.get_student(student_username)
    except UserNotFoundException:
        raise ValueError()

    slot_service = SlotService(session)
    assigned_slot = await slot_service.assign_slot(student.uuid, slot_uuid)

    await callback.message.answer(
        bt.SLOTS_ASSIGN_SUCCESS_ANSWER.format(
            assigned_slot.uuid_teacher,
            assigned_slot.dt_start.strftime(full_format_no_sec)
        )
    )
    await callback.answer()
