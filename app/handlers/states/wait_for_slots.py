from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.is_slots_correct import get_is_slots_correct_markup
from app.states.schedule_states import ScheduleStates
from app.utils.parse_slots import parse_slots

router = Router()


@router.message(ScheduleStates.wait_for_slots)
async def wait_for_slots(message: Message, state: FSMContext):
    slots_raw = message.text
    await message.answer("Получил, обрабатываю")
    parsed_lessons = parse_slots(slots_raw, message.from_user.username)
    await message.answer("Обработал!")
    slot_message = ""
    for slot in parsed_lessons:
        slot_message += (f"📅: {slot.day_name}, {slot.slot_date}\n"
                         f"🕐: {", ".join(map(lambda slot_time: slot_time.strftime("%H:%M"), slot.available_time))}\n\n")
    slot_message += "Верно?"
    await message.answer(slot_message, reply_markup=get_is_slots_correct_markup())
    await state.clear()
