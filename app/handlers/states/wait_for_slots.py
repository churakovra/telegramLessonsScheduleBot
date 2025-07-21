from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.slot_service import SlotService
from app.states.schedule_states import ScheduleStates
from app.utils.keyboards.is_slots_correct import get_is_slots_correct_markup

router = Router()


@router.message(ScheduleStates.wait_for_slots)
async def wait_for_slots(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    teacher_uuid = data["teacher_uuid"]
    previous_message_id = data["previous_message_id"]

    slots_raw = message.text

    slot_service = SlotService(session)
    slots = await slot_service.parse_slots(slots_raw, teacher_uuid)
    await state.update_data(slots=slots)

    await state.set_state(ScheduleStates.wait_for_confirmation)
    await message.chat.delete_message(previous_message_id)

    slot_reply = await slot_service.get_slot_reply(slots)
    markup = get_is_slots_correct_markup()
    await message.answer(text=slot_reply, reply_markup=markup)

    await state.update_data(previous_message_id=message.message_id)
