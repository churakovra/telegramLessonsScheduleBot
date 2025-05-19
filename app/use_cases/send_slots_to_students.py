from app.models.teacher_slot import Slot
from app.notifiers.telegram_notifier import TelegramNotifier
from app.services.teacher_service import TeacherService


async def send_slots_to_students_use_case(slots: list[Slot], notifier: TelegramNotifier):
    teacher = slots[0].teacher
    students = await TeacherService.get_students(teacher)
    pass
