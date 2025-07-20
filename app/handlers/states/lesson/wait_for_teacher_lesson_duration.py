from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.config.logger import setup_logger

router = Router()
logger = setup_logger("teacher-lesson-duration")


@router.message(ScheduleStates.wait_for_teacher_lesson_duration)
async def handle_state(
        message: Message,
        state: FSMContext
):
    data = await state.get_data()
    previous_message_id = data["previous_message_id"]
    try:
        duration = int(message.text.strip())
        await state.update_data(lesson_duration=duration)
        await state.set_state(ScheduleStates.wait_for_teacher_lesson_price)

        sent_message = await message.answer(BotStrings.TEACHER_ADD_LESSON_PRICE)
        await state.update_data(previous_message_id=sent_message.message_id)

    except Exception as e:
        logger.error(e)

        await state.set_state(ScheduleStates.wait_for_teacher_lesson_duration)

        sent_message = await message.answer(BotStrings.TEACHER_ADD_LESSON_DURATION_ERROR)
        await state.update_data(previous_message_id=sent_message.message_id)

    finally:
        await message.chat.delete_message(message_id=previous_message_id)
        await message.delete()
