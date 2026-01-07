from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.slot_dto import CreateSlotDTO
from app.services.slot_service import SlotService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import OperationType
from app.utils.keyboards.markup_builder import MarkupBuilder
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


router = Router()


@router.callback_query(
    F.data == BotStrings.Teacher.CALLBACK_SLOTS_CORRECT,
    ScheduleStates.wait_for_confirmation,
)
async def reply_and_save_to_db(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    data = await state.get_data()
    slots: list[CreateSlotDTO] = data["slots"]
    teacher_uuid = data["teacher_uuid"]
    operation_type = data["operation_type"]
    
    slot_service = SlotService(session)
    if operation_type == OperationType.ADD:
        await slot_service.add_slots(slots)
    elif operation_type == OperationType.UPDATE:
        await slot_service.update_slots(slots=slots, teacher_uuid=teacher_uuid)
    else:
        logger.error("Unknown type of operation")
        await callback.message.answer(
            text="Unknown type of operation",
        )
    logger.info(f"Teacher {teacher_uuid} successfully added slots")
    await callback.message.answer(
        text=BotStrings.Teacher.SLOTS_PROCESSING_SUCCESS,
        reply_markup=MarkupBuilder.send_slots_markup(
            teacher_uuid=teacher_uuid, operation_type=operation_type
        ),
    )

    await state.clear()
    await callback.answer()
