from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.keyboard.callback_factories.menu import ConfirmMenuCallback
from app.keyboard.fabric import send_slots
from app.message.models import BotMessage
from app.schemas.slot import CreateSlotDTO
from app.services.container import Services
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.datetime_utils import full_format_no_sec
from app.utils.exceptions.slot_exceptions import SlotConflictException
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.callback_query(
    ConfirmMenuCallback.filter(F.confirm.is_(True)),
    ScheduleStates.wait_for_confirmation,
)
async def reply_and_save_to_db(
    callback: CallbackQuery, state: FSMContext, services: Services
):
    data = await state.get_data()
    slots: list[CreateSlotDTO] = data["slots"]
    teacher_uuid = data["teacher_uuid"]
    action = data["action"]

    try:
        if action == "Create":
            await services.slot.add_slots(slots)
        else:
            await services.slot.update_slots(slots, teacher_uuid)
    except SlotConflictException as e:
        conflicted_slots = "\n".join(
            f"• {dt_start.strftime(full_format_no_sec)}"
            for dt_start in e.conflicted_datetimes
        )
        message = BotMessage(
            text=BotStrings.Teacher.SLOTS_CONFLICT.format(slots=conflicted_slots)
        )
        await callback.message.answer(**message.to_aiogram_kwargs())
        await state.set_state(ScheduleStates.wait_for_slots)
        await callback.answer()
        return

    logger.info(f"Teacher {teacher_uuid} successfully added slots")

    markup = send_slots(teacher_uuid=teacher_uuid)
    message = BotMessage(
        text=BotStrings.Teacher.SLOTS_PROCESSING_SUCCESS, markup=markup
    )
    await callback.message.answer(**message.to_aiogram_kwargs())
    await state.clear()
    await callback.answer()


@router.callback_query(
    ConfirmMenuCallback.filter(F.confirm.is_(False)),
    ScheduleStates.wait_for_confirmation,
)
async def handle_callback(callback: CallbackQuery, state: FSMContext):
    message = BotMessage(text=BotStrings.Teacher.SLOTS_FAILURE)
    await callback.message.answer(**message.to_aiogram_kwargs())
    await state.set_state(ScheduleStates.wait_for_slots)
    await callback.message.delete()
    await callback.answer()
