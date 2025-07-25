from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.notifiers.telegram_notifier import TelegramNotifier
from app.schemas.bot_message import BotMessage
from app.services.slot_service import SlotService
from app.services.teacher_service import TeacherService
from app.services.user_service import UserService
from app.utils.exceptions.teacher_exceptions import TeacherStudentsNotFound
from app.utils.keyboards.callback_factories.send_slots import SendSlotsCallback
from app.utils.keyboards.days_for_students_markup import get_days_for_students_markup
from app.utils.message_template import MessageTemplate

router = Router()


@router.callback_query(SendSlotsCallback.filter())
async def handle_callback(
        callback: CallbackQuery,
        callback_data: SendSlotsCallback,
        session: AsyncSession,
        notifier: TelegramNotifier
):
    teacher_uuid = callback_data.teacher_uuid
    teacher_service = TeacherService(session)
    slots_service = SlotService(session)

    try:
        students = await teacher_service.get_unsigned_students(teacher_uuid)

        slots = await slots_service.get_free_slots(teacher_uuid)
        message_text = await slots_service.get_slot_reply(slots)
        markup = get_days_for_students_markup(slots, teacher_uuid)

        message = BotMessage(
            message_text=message_text,
            reply_markup=markup
        )
        await notifier.send_message_to_users(message, students)
        await callback.message.delete()

    except TeacherStudentsNotFound as e:
        await callback.message.answer(e.message)
    finally:
        user_service = UserService(session)
        user, markup = await user_service.get_user_menu(callback.from_user.username)
        bot_message = MessageTemplate.get_menu_message(user.username, markup)
        await notifier.send_message(
            bot_message=bot_message,
            receiver_chat_id=callback.message.chat.id
        )

        await callback.answer()
