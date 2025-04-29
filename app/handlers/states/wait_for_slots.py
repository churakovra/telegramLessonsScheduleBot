from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.is_slots_correct import get_is_slots_correct_markup
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import bot_strings as bt
from app.utils.create_parsed_slots_message_text import create_parsed_slots_message_text
from app.utils.parse_slots import parse_slots

router = Router()


@router.message(ScheduleStates.wait_for_slots)
async def wait_for_slots(message: Message, state: FSMContext):
    slots_raw = message.text
    await message.answer(bt.PARSING_SLOTS_PROCESSING)
    parsed_lessons = await parse_slots(slots_raw, message.from_user.username)
    await message.answer(bt.PARSING_SLOTS_SUCCESS)
    slot_message = create_parsed_slots_message_text(parsed_lessons)
    await message.answer(slot_message, reply_markup=get_is_slots_correct_markup())
    await state.clear()
