from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.slot_service import SlotService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.keyboards.send_slots_markup import get_send_slots_markup

router = Router()


@router.callback_query(F.data == BotStrings.CALLBACK_SLOTS_CORRECT, ScheduleStates.wait_for_confirmation)
async def reply_and_save_to_db(
        callback: CallbackQuery,
        state: FSMContext,
        session: AsyncSession
):
    data = await state.get_data()
    slots = data["slots"]
    teacher_uuid = data["teacher_uuid"]
    previous_message_id = data["previous_message_id"]

    slot_service = SlotService(session)
    await slot_service.add_slots(slots)
    await callback.message.answer(
        text=bt.SLOTS_PROCESSING_SUCCESS_ANSWER,
        reply_markup=get_send_slots_markup(teacher_uuid)
    )

    await callback.message.chat.delete_message(previous_message_id)
    await callback.message.delete()
    await state.clear()
    await callback.answer()
