from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import KeyboardType, OperationType
from app.utils.enums.menu_type import MenuType
from app.utils.keyboard.callback_factories.menu import MenuCallback
from app.utils.keyboard.callback_factories.slots import SlotsUpdate
from app.utils.keyboard.builder import MarkupBuilder
from app.utils.keyboard.context import SpecifyWeekKeyboardContext
from app.utils.logger import setup_logger
from app.utils.message_template import specify_week_message

logger = setup_logger(__name__)

router = Router()


@router.callback_query(MenuCallback.filter(F.menu_type == MenuType.TEACHER_SLOT_UPDATE))
async def on_teacher_slot_update(callback: CallbackQuery):
    markup_context = SpecifyWeekKeyboardContext(SlotsUpdate)
    markup = MarkupBuilder.build(KeyboardType.SPECIFY_WEEK, markup_context)
    message = specify_week_message(markup)
    await callback.message.answer(**message)
    await callback.answer()


@router.callback_query(SlotsUpdate.filter())
async def handle_callback(
    callback: CallbackQuery, callback_data: SlotsUpdate, state: FSMContext
):
    await state.set_state(ScheduleStates.wait_for_slots)
    await state.update_data(week_flag=callback_data.week_flag)
    await state.update_data(operation_type=OperationType.UPDATE)
    await callback.message.answer(BotStrings.Teacher.SLOTS_ADD)
    await callback.answer()
