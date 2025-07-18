from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.keyboards.is_slots_correct import get_is_slots_correct_markup
from app.services.slot_service import SlotService
from app.services.teacher_service import TeacherService
from app.states.schedule_states import ScheduleStates

router = Router()


@router.message(ScheduleStates.wait_for_slots)
async def wait_for_slots(message: Message, state: FSMContext, session: AsyncSession):
    slots_raw = message.text
    message_from = message.from_user.username

    teacher_service = TeacherService(session)
    teacher = await teacher_service.get_teacher(message_from)

    slot_service = SlotService(session)
    slots = await slot_service.parse_slots(slots_raw, teacher.uuid)

    slot_reply = await slot_service.get_slot_reply(slots)
    await message.answer(
        text=slot_reply,
        reply_markup=get_is_slots_correct_markup()
    )

    await state.update_data(slots=slots, teacher=teacher)
    await state.set_state(ScheduleStates.wait_for_confirmation)
