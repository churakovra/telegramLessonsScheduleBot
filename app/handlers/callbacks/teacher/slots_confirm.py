from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboard.builder import MarkupBuilder
from app.keyboard.callback_factories.menu import ConfirmMenuCallback
from app.keyboard.context import SendSlotsKeyboardContext
from app.schemas.slot_dto import CreateSlotDTO
from app.services.slot_service import SlotService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import KeyboardType
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.callback_query(
    ConfirmMenuCallback.filter(F.confirm == True),
    ScheduleStates.wait_for_confirmation,
)
async def reply_and_save_to_db(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    data = await state.get_data()
    slots: list[CreateSlotDTO] = data["slots"]
    teacher_uuid = data["teacher_uuid"]

    slot_service = SlotService(session)
    await slot_service.add_slots(slots)
    logger.info(f"Teacher {teacher_uuid} successfully added slots")
    markup_context = SendSlotsKeyboardContext(teacher_uuid)
    await callback.message.answer(
        text=BotStrings.Teacher.SLOTS_PROCESSING_SUCCESS,
        reply_markup=MarkupBuilder.build(KeyboardType.SEND_SLOTS, markup_context),
    )

    await state.clear()
    await callback.answer()


@router.callback_query(ConfirmMenuCallback.filter(F.confirm == False))
async def handle_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(BotStrings.Teacher.SLOTS_FAILURE)
    await state.set_state(ScheduleStates.wait_for_slots)
    await callback.message.delete()
    await callback.answer()
