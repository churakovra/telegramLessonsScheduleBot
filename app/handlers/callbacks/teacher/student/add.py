from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.teacher_service import TeacherService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.enums.menu_type import MenuType
from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.utils.keyboard.callback_factories.menu import MenuCallback

router = Router()


@router.callback_query(MenuCallback.filter(F.menu_type == MenuType.TEACHER_STUDENT_ADD))
async def handle_callback(
        callback: CallbackQuery,
        session: AsyncSession,
        state: FSMContext
):
    teacher_service = TeacherService(session)
    try:
        teacher = await teacher_service.get_teacher(callback.from_user.username)

        await state.update_data(teacher_uuid=teacher.uuid)
        await state.set_state(ScheduleStates.wait_for_teacher_students)

        message = await callback.message.answer(BotStrings.Teacher.TEACHER_STUDENT_ADD)
        await state.update_data(previous_message_id=message.message_id)

    except UserNotFoundException:
        await callback.message.answer(BotStrings.Teacher.NOT_ENOUGH_RIGHTS)
        return
    finally:
        await callback.message.delete()
        await callback.answer()
