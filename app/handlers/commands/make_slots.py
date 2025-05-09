from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.handlers.commands.slots_error import send_slots_error
from app.keyboards.is_slots_correct import get_is_slots_correct_markup
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import bot_strings as bt
from app.utils.bot_values import BotValues
from app.utils.create_parsed_slots_message_text import create_parsed_slots_message_text
from app.utils.parse_slots import parse_slots

router = Router()

roles = BotValues.UserRoles


@router.message(Command("make_slots"))
async def make_slots(message: Message, state: FSMContext):
    slots_raw = message.text
    await message.answer(bt.PARSING_SLOTS_PROCESSING)
    parsed_lessons = await parse_slots(slots_raw, message.from_user.username)
    if parsed_lessons:
        slot_message = create_parsed_slots_message_text(parsed_lessons)
        await message.answer(bt.PARSING_SLOTS_SUCCESS)
        await message.answer(slot_message, reply_markup=get_is_slots_correct_markup())
        await state.update_data(parsed_lessons=parsed_lessons)
        await state.set_state(ScheduleStates.wait_for_confirmation)
    else:
        await send_slots_error(message, state)
