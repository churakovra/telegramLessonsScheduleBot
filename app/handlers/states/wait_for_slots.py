from aiogram import Router
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboard.builder import MarkupBuilder
from app.services.slot_service import SlotService
from app.services.teacher_service import TeacherService
from app.states.schedule_states import ScheduleStates
from app.utils.enums.bot_values import KeyboardType
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.message(
    or_f(
        ScheduleStates.wait_for_slots,
        ScheduleStates.wait_for_slots_update,
    )
)
async def wait_for_slots(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    week_flag = data["week_flag"]
    slots_raw = message.text
    teacher_service = TeacherService(session)
    teacher = await teacher_service.get_teacher(message.from_user.username)
    slot_service = SlotService(session)
    slots = await slot_service.parse_slots(
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
    slot_reply = await slot_service.get_parsed_slots_reply(slots)
    markup = MarkupBuilder.build(KeyboardType.IS_SLOTS_CORRECT)
    await message.answer(text=slot_reply, reply_markup=markup)
