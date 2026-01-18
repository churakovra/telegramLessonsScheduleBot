from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.lesson_service import LessonService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.logger import setup_logger


router = Router()
logger = setup_logger(__name__)



@router.message(ScheduleStates.wait_for_lesson_update)
async def handle_state(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    lesson_uuid = data["lesson_uuid"]
    spec = data["spec"]
    new_value = message.text.strip()
    lesson_service = LessonService(session)
    await lesson_service.update_lesson(lesson_uuid, **{spec:new_value})
    await message.answer(BotStrings.Teacher.TEACHER_LESSON_UPDATE_SUCCESS)
    await state.clear()