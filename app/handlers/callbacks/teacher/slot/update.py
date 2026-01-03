from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import OperationType
from app.utils.enums.menu_type import MenuType
from app.utils.keyboards.callback_factories.menu import SubMenu
from app.utils.keyboards.callback_factories.slots import UpdateSlots
from app.utils.keyboards.markup_builder import MarkupBuilder
from app.utils.logger import setup_logger
from app.utils.message_template import MessageTemplate

logger = setup_logger(__name__)

router = Router()


@router.callback_query(SubMenu.filter(F.menu_type == MenuType.TEACHER_SLOT_UPDATE))
async def on_teacher_slot_update(callback: CallbackQuery):
    markup = MarkupBuilder.specify_week_markup(callback_data=UpdateSlots)
    message = MessageTemplate.specify_week_message(markup)
    await callback.message.answer(
        text=message.message_text, reply_markup=message.reply_markup
    )
    await callback.answer()


@router.callback_query(UpdateSlots.filter())
async def handle_callback(
    callback: CallbackQuery, callback_data: UpdateSlots, state: FSMContext
):
    await state.set_state(ScheduleStates.wait_for_slots)
    await state.update_data(week_flag=callback_data.week_flag)
    await state.update_data(operation_type=OperationType.UPDATE)
    await callback.message.answer(BotStrings.Teacher.SLOTS_ADD)
    await callback.answer()
