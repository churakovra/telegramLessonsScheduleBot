from uuid import UUID

from app.keyboards.days_for_students_markup import get_days_for_students_markup
from app.models.BotMessage import BotMessage
from app.notifiers.telegram_notifier import TelegramNotifier
from app.services.teacher_service import TeacherService


async def send_slots_to_students_use_case(
        teacher: str,
        slots: dict[str, UUID],
        parsed_slots: str,
        notifier: TelegramNotifier
):
    students = await TeacherService.get_students(teacher)
    markup = get_days_for_students_markup(slots)
    for student in students:
        bot_message = BotMessage(
            receiver_user_id=student.id,
            receiver_username=student.username,
            receiver_chat_id=student.chat_id,
            message_text=parsed_slots,
            reply_markup=markup
        )
        await notifier.send_message(bot_message)
