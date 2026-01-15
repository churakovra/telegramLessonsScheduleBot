from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.teacher_service import TeacherService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import OperationType
from app.utils.enums.menu_type import MenuType
from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.keyboard.callback_factories.menu import MenuCallback
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)

@router.callback_query(MenuCallback.filter(F.menu_type == MenuType.TEACHER_LESSON_ADD))
async def handle_callback(
        callback: CallbackQuery,
        session: AsyncSession,
        state: FSMContext
):
    teacher_service = TeacherService(session)
    try:
        teacher = await teacher_service.get_teacher(callback.from_user.username)
        await state.update_data(uuid_teacher=teacher.uuid)
        await state.update_data(operation_type=OperationType.ADD)
        await state.set_state(ScheduleStates.wait_for_teacher_lesson_label)
        await callback.message.delete()
        message = await callback.message.answer(BotStrings.Teacher.TEACHER_LESSON_ADD_LABEL)
        await state.update_data(previous_message_id=message.message_id)
    except UserNotFoundException:
        logger.error(f"Teacher {teacher.uuid} tried to add new lesson, but didn't have enough rights")
        await callback.message.answer(BotStrings.Teacher.NOT_ENOUGH_RIGHTS)
        return
    finally:
        await callback.answer()

