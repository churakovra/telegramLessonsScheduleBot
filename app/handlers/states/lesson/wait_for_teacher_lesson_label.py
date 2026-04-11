from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboard import fabric
from app.message.models import BotMessage
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.message(ScheduleStates.wait_for_teacher_lesson_label)
async def handle_state(message: Message, state: FSMContext):
    raw_mt = getattr(message, "text", "")
    lesson_label = raw_mt.strip()
    await state.update_data(lesson_label=lesson_label)
    await state.set_state(ScheduleStates.wait_for_teacher_lesson_duration)

    data = await state.get_data()
    previous_message_id = data["previous_message_id"]
    await message.chat.delete_message(previous_message_id)
    await message.delete()

    msg = BotMessage(
        text=BotStrings.Teacher.TEACHER_LESSON_ADD_DURATION,
        markup=fabric.cancel_markup(),
    )
    sent_message = await message.answer(**msg.to_dict())
    await state.update_data(previous_message_id=sent_message.message_id)
