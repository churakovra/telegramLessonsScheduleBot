from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboard import fabric
from app.message.models import BotMessage
from app.services.container import Services
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import ActionType
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.message(ScheduleStates.wait_for_teacher_lesson_price)
async def handle_state(
    message: Message,
    services: Services,
    state: FSMContext,
):
    data = await state.get_data()
    previous_message_id = data["previous_message_id"]
    operation_type = data["operation_type"]
    raw_mt = getattr(message, "text", "")

    label = data["lesson_label"]
    duration = data["lesson_duration"]
    price = int(raw_mt.strip())
    uuid_teacher = data["uuid_teacher"]

    try:
        if operation_type == ActionType.CREATE:
            await services.lesson.create_lesson(
                label=label, duration=duration, uuid_teacher=uuid_teacher, price=price
            )
            response_msg = BotStrings.Teacher.TEACHER_LESSON_ADD_SUCCESS
        else:
            uuid_lesson = data["uuid_lesson"]
            await services.lesson.update_lesson(
                lesson_uuid=uuid_lesson, label=label, duration=duration, price=price
            )
            response_msg = BotStrings.Teacher.TEACHER_LESSON_UPDATE_SUCCESS

        reply_message = BotMessage(text=response_msg, markup=fabric.teacher_main_menu())
        await message.answer(**reply_message.to_aiogram_kwargs())
        await state.clear()

        logger.info(f"Teacher {uuid_teacher} added new lesson")
    except Exception:
        logger.error(type)
        error_message = BotMessage(
            text=BotStrings.Teacher.TEACHER_LESSON_ADD_PRICE_ERROR
        )
        sent_message = await message.answer(**error_message.to_aiogram_kwargs())
        await state.update_data(previous_message_id=sent_message.message_id)
        await state.set_state(ScheduleStates.wait_for_teacher_lesson_price)

    finally:
        await message.chat.delete_message(message_id=previous_message_id)
        await message.delete()
