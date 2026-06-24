from aiogram import Router
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboard import fabric
from app.message.models import BotMessage
from app.message.utils import slots_to_reply
from app.services.container import Services
from app.states.schedule_states import ScheduleStates
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.message(
    or_f(
        ScheduleStates.wait_for_slots,
        ScheduleStates.wait_for_slots_update,
    )
)
async def wait_for_slots(message: Message, state: FSMContext, services: Services):
    data = await state.get_data()
    week_flag = data["week_flag"]
    slots_raw = message.text
    teacher = await services.teacher.get_teacher(message.from_user.username)
    slots = await services.slot.parse_slots(
        message_text=slots_raw, uuid_teacher=teacher.uuid, week_flag=week_flag
    )
    action = (
        "Create"
        if await state.get_state() == "ScheduleStates:wait_for_slots"
        else "Update"
    )
    await state.set_state(ScheduleStates.wait_for_confirmation)
    await state.update_data(teacher_uuid=teacher.uuid)
    await state.update_data(slots=slots)
    await state.update_data(action=action)
    markup = fabric.parsed_slots()
    msg = BotMessage(text=slots_to_reply(slots), markup=markup)
    await message.answer(**msg.to_aiogram_kwargs())
