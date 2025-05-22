from uuid import UUID

from app.keyboards.days_for_students_markup import get_days_for_students_markup
from app.notifiers.telegram_notifier import TelegramNotifier
from app.services.teacher_service import TeacherService


async def send_slots_to_students_use_case(
        teacher: str,
        slots: dict[str, UUID],
        notifier: TelegramNotifier
):
    students = await TeacherService.get_students(teacher)
    markup = get_days_for_students_markup(slots)
    for student in students:
        await notifier.send_message(
            student.chat_id,
            f"Сообщение от нотифаера, {teacher} - учитель",
            reply_markup=markup
        )
