from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings

router = Router()

@router.message(ScheduleStates.wait_for_teacher_lesson_duration)
async def handle_state(
        message: Message,
        state: FSMContext
):
    try:
        duration = int(message.text.strip())
        await state.update_data(lesson_duration=duration)
        await state.set_state(ScheduleStates.wait_for_teacher_lesson_price)

        data = await state.get_data()
        previous_message_id = data["previous_message_id"]
        await message.chat.delete_message(message_id=previous_message_id)
        await message.delete()

        message = await message.answer(BotStrings.TEACHER_ADD_LESSON_PRICE)
        await state.update_data(previous_message_id=message.message_id)

    except Exception as e:
        await message.answer(str(e))
