from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.is_slots_correct import get_is_slots_correct_markup
from app.states.schedule_states import ScheduleStates
from app.use_cases.set_new_slots import set_new_slots_use_case
from app.utils.create_parsed_slots_message_text import create_parsed_slots_message_text

router = Router()


@router.message(ScheduleStates.wait_for_slots)
async def wait_for_slots(message: Message, state: FSMContext):
    slots_raw = message.text
    message_from = message.from_user.username
    slots = await set_new_slots_use_case(slots_raw, message_from)

    slots_reply = create_parsed_slots_message_text(slots)
    await message.answer(
        text=slots_reply,
        reply_markup=get_is_slots_correct_markup()
    )

    await state.update_data(slots=slots)
    await state.set_state(ScheduleStates.wait_for_confirmation)
