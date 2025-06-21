from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.orm import Session

from app.services.slot_service import SlotService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import bot_strings as bt

router = Router()


@router.callback_query(F.data == bt.CALLBACK_SLOTS_CORRECT, ScheduleStates.wait_for_confirmation)
async def reply_and_save_to_db(callback: CallbackQuery, state: FSMContext, session: Session):
    """
    Удалил отсюда отправку слотов ученикам. После записи в БД нужно переходить в стейт NewSlotsAreReady или как-то так
    и отправлять это дело ученикам из специализированного метода
    """

    data = await state.get_data()
    slots = data.get("slots")
    teacher = data.get("teacher")

    slot_service = SlotService(session)
    slot_service.add_slots(slots)
    await callback.message.answer(
        text=bt.SLOTS_PROCESSING_SUCCESS_ANSWER
    )
    await callback.answer()
