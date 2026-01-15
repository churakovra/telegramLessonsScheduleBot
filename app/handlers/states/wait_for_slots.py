from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.slot_service import SlotService
from app.services.teacher_service import TeacherService
from app.states.schedule_states import ScheduleStates
from app.utils.enums.bot_values import KeyboardType
from app.keyboard.builder import MarkupBuilder
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.message(ScheduleStates.wait_for_slots)
async def wait_for_slots(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    week_flag = data["week_flag"]

    slots_raw = getattr(message, "text", "")

    teacher_service = TeacherService(session)
    teacher = await teacher_service.get_teacher(message.from_user.username)

    slot_service = SlotService(session)
    slots = await slot_service.parse_slots(
        message_text=slots_raw, uuid_teacher=teacher.uuid, week_flag=week_flag
    )
    await state.update_data(slots=slots)

    await state.set_state(ScheduleStates.wait_for_confirmation)

    slot_reply = await slot_service.get_parsed_slots_reply(slots)
    markup = MarkupBuilder.build(KeyboardType.IS_SLOTS_CORRECT)
    await message.answer(text=slot_reply, reply_markup=markup)

    await state.update_data(teacher_uuid=teacher.uuid)
