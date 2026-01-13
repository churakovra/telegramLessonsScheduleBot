from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.notifiers.telegram_notifier import TelegramNotifier
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import OperationType, WeekFlag
from app.utils.enums.menu_type import MenuType
from app.utils.keyboard.callback_factories.menu import MenuCallback
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)

@router.callback_query(MenuCallback.filter(F.menu_type == MenuType.TEACHER_SLOT_ADD))
async def handle_callback(
    callback: CallbackQuery,
    session: AsyncSession,
    state: FSMContext,
    notifier: TelegramNotifier,
):
    await state.set_state(ScheduleStates.wait_for_slots)
    await state.update_data(week_flag=WeekFlag.NEXT)
    await state.update_data(operation_type=OperationType.ADD)
    await callback.message.answer(BotStrings.Teacher.SLOTS_ADD)
    await callback.answer()
    logger.info("Add slot flow has been started")
