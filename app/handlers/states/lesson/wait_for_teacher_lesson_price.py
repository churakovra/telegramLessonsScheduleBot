from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboard import markup_type_by_role
from app.keyboard.builder import MarkupBuilder
from app.notifier.telegram_notifier import TelegramNotifier
from app.services.lesson_service import LessonService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import ActionType, UserRole
from app.utils.logger import setup_logger
from app.utils.message_template import main_menu_message

router = Router()
logger = setup_logger(__name__)


@router.message(ScheduleStates.wait_for_teacher_lesson_price)
async def handle_state(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    notifier: TelegramNotifier,
):
    data = await state.get_data()
    previous_message_id = data["previous_message_id"]
    operation_type = data["operation_type"]
    raw_mt = getattr(message, "text", "")
    username = getattr(message.from_user, "username", "") or ""

    label = data["lesson_label"]
    duration = data["lesson_duration"]
    price = int(raw_mt.strip())
    uuid_teacher = data["uuid_teacher"]

    try:
        lesson_service = LessonService(session)
        if operation_type == ActionType.CREATE:
            await lesson_service.create_lesson(
                label=label, duration=duration, uuid_teacher=uuid_teacher, price=price
            )
            response_msg = BotStrings.Teacher.TEACHER_LESSON_ADD_SUCCESS
        else:
            uuid_lesson = data["uuid_lesson"]
            await lesson_service.update_lesson(
                lesson_uuid=uuid_lesson, label=label, duration=duration, price=price
            )
            response_msg = BotStrings.Teacher.TEACHER_LESSON_UPDATE_SUCCESS

        await message.answer(str.format(response_msg))

        markup = MarkupBuilder.build(markup_type_by_role[UserRole.TEACHER])
        bot_message = main_menu_message(markup)
        await notifier.send_message(
            bot_message=bot_message, receiver_chat_id=message.chat.id
        )
        await state.clear()

        logger.info(f"Teacher {uuid_teacher} added new lesson")
    except Exception as e:
        logger.error(type)

        sent_message = await message.answer(
            BotStrings.Teacher.TEACHER_LESSON_ADD_PRICE_ERROR
        )
        await state.update_data(previous_message_id=sent_message.message_id)
        await state.set_state(ScheduleStates.wait_for_teacher_lesson_price)

    finally:
        await message.chat.delete_message(message_id=previous_message_id)
        await message.delete()
