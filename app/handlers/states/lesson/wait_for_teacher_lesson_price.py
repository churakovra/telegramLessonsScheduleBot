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

from ._helpers import delete_previous_messages, send_next_prompt

router = Router()
logger = setup_logger(__name__)


@router.message(ScheduleStates.wait_for_teacher_lesson_price)
async def handle_state(
    message: Message,
    services: Services,
    state: FSMContext,
):
    data = await state.get_data()
    operation_type = data["operation_type"]
    raw_mt = message.text or ""

    label = data["lesson_label"]
    duration = data["lesson_duration"]
    uuid_teacher = data["uuid_teacher"]

    try:
        price = int(raw_mt.strip())

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
        await delete_previous_messages(message, state)
        await state.clear()

        logger.info(f"Teacher {uuid_teacher} added new lesson")
    except ValueError:
        logger.warning(f"Invalid price input from user: {raw_mt!r}")
        await delete_previous_messages(message, state)
        await send_next_prompt(
            message=message,
            state=state,
            next_state=ScheduleStates.wait_for_teacher_lesson_price,
            prompt_text=BotStrings.Teacher.TEACHER_LESSON_ADD_PRICE_ERROR,
        )
    except Exception:
        logger.exception("Failed to process lesson price")
        await delete_previous_messages(message, state)
        await send_next_prompt(
            message=message,
            state=state,
            next_state=ScheduleStates.wait_for_teacher_lesson_price,
            prompt_text=BotStrings.Teacher.TEACHER_LESSON_ADD_PRICE_ERROR,
        )
