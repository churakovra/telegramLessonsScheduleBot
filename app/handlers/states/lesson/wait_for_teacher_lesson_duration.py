from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboard import fabric
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.logger import setup_logger

from ._helpers import delete_previous_messages, send_next_prompt

router = Router()
logger = setup_logger(__name__)


@router.message(ScheduleStates.wait_for_teacher_lesson_duration)
async def handle_state(message: Message, state: FSMContext):
    raw_mt = message.text or ""
    try:
        duration = int(raw_mt.strip())
        await state.update_data(lesson_duration=duration)
        await delete_previous_messages(message, state)
        await send_next_prompt(
            message=message,
            state=state,
            next_state=ScheduleStates.wait_for_teacher_lesson_price,
            prompt_text=BotStrings.Teacher.TEACHER_LESSON_ADD_PRICE,
            markup=fabric.cancel_markup(),
        )

    except ValueError as e:
        logger.error(e)
        await delete_previous_messages(message, state)
        await send_next_prompt(
            message=message,
            state=state,
            next_state=ScheduleStates.wait_for_teacher_lesson_duration,
            prompt_text=BotStrings.Teacher.TEACHER_LESSON_ADD_DURATION_ERROR,
        )
