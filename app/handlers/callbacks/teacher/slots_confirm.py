from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboard.callback_factories.menu import ConfirmMenuCallback
from app.keyboard.callback_factories.slot import SendSlots
from app.keyboard.fabric import send_slots
from app.message.models import BotMessage
from app.schemas.slot import CreateSlotDTO
from app.services.slot_service import SlotService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.callback_query(
    ConfirmMenuCallback.filter(F.confirm.is_(True)),
    ScheduleStates.wait_for_confirmation,
)
async def reply_and_save_to_db(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    data = await state.get_data()
    slots: list[CreateSlotDTO] = data["slots"]
    teacher_uuid = data["teacher_uuid"]
    action = data["action"]

    slot_service = SlotService(session)
    if action == "Create":
        await slot_service.add_slots(slots)
    else:
        await slot_service.update_slots(slots, teacher_uuid)

    logger.info(f"Teacher {teacher_uuid} successfully added slots")

    markup = send_slots(type("Context", (), {"teacher_uuid": teacher_uuid})())
    message = BotMessage(
        text=BotStrings.Teacher.SLOTS_PROCESSING_SUCCESS, markup=markup
    )
    await callback.message.answer(**message.to_aiogram_kwargs())
    await state.clear()
    await callback.answer()


@router.callback_query(ConfirmMenuCallback.filter(F.confirm.is_(False)))
async def handle_callback(callback: CallbackQuery, state: FSMContext):
    message = BotMessage(text=BotStrings.Teacher.SLOTS_FAILURE)
    await callback.message.answer(**message.to_aiogram_kwargs())
    await state.set_state(ScheduleStates.wait_for_slots)
    await callback.message.delete()
    await callback.answer()
