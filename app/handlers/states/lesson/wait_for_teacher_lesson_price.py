from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.lesson_service import LessonService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.config.logger import setup_logger

router = Router()
logger = setup_logger("lesson_price")

@router.message(ScheduleStates.wait_for_teacher_lesson_price)
async def handle_state(
        message: Message,
        session: AsyncSession,
        state: FSMContext
):
    try:
        price = int(message.text.strip())

        data = await state.get_data()
        lesson = {
            "label": data["lesson_label"],
            "duration": data["lesson_duration"],
            "price": price,
            "uuid_teacher": data["teacher_uuid"],
        }
        logger.debug(lesson)

        lesson_service = LessonService(session)
        await lesson_service.create_lesson(**lesson)

        previous_message_id = data["previous_message_id"]
        await message.chat.delete_message(message_id=previous_message_id)
        await message.delete()

        await message.answer(str.format(BotStrings.TEACHER_ADD_LESSON_SUCCESS, lesson["label"]))
        await state.clear()

    except Exception as e:
        await message.answer(str(e))

