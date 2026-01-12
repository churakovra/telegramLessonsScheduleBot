from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.enums.menu_type import MenuType
from app.utils.keyboard.callback_factories.menu import SubMenu

router = Router()


@router.callback_query(SubMenu.filter(F.menu_type == MenuType.TEACHER_STUDENT_DELETE))
async def handle_callback(
        callback: CallbackQuery,
        state: FSMContext
):
    await state.set_state(ScheduleStates.wait_for_student_to_delete)
    await callback.message.delete()
    await callback.message.answer(BotStrings.Teacher.TEACHER_STUDENT_DELETE)
