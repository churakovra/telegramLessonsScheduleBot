from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.notifiers.telegram_notifier import TelegramNotifier
from app.services.lesson_service import LessonService
from app.services.user_service import UserService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.config.logger import setup_logger
from app.utils.message_template import MessageTemplate

router = Router()
logger = setup_logger("teacher-lesson-price")


@router.message(ScheduleStates.wait_for_teacher_lesson_price)
async def handle_state(
        message: Message,
        session: AsyncSession,
        state: FSMContext,
        notifier: TelegramNotifier
):
    data = await state.get_data()
    previous_message_id = data["previous_message_id"]
    raw_mt = getattr(message, "text", "")
    username = getattr(message.from_user, "username", "") or ""
    try:
        price = int(raw_mt.strip())

        lesson = {
            "label": data["lesson_label"],
            "duration": data["lesson_duration"],
            "price": price,
            "uuid_teacher": data["teacher_uuid"],
        }
        logger.debug(lesson)

        lesson_service = LessonService(session)
        await lesson_service.create_lesson(**lesson)

        await message.answer(str.format(BotStrings.TEACHER_LESSON_ADD_SUCCESS, lesson["label"]))

        user_service = UserService(session)
        user, markup = await user_service.get_user_menu(username)
        bot_message = MessageTemplate.get_menu_message(user.username, markup)
        await notifier.send_message(
            bot_message=bot_message,
            receiver_chat_id=message.chat.id
        )
        await state.clear()

    except Exception as e:
        logger.error(e)

        sent_message = await message.answer(BotStrings.TEACHER_LESSON_ADD_PRICE_ERROR)
        await state.update_data(previous_message_id=sent_message.message_id)
        await state.set_state(ScheduleStates.wait_for_teacher_lesson_price)

    finally:
        await message.chat.delete_message(message_id=previous_message_id)
        await message.delete()
