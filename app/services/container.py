from app.database.unit_of_work import UnitOfWork
from app.services.feedback_service import FeedbackService
from app.services.lesson_service import LessonService
from app.services.notification_service import NotificationService
from app.services.recurrence_service import RecurrenceService
from app.services.reschedule_service import RescheduleService
from app.services.slot_service import SlotService
from app.services.statistics_service import StatisticsService
from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.services.user_service import UserService


class Services:
    def __init__(self, uow: UnitOfWork) -> None:
        self.user = UserService(repository=uow.users)
        self.teacher = TeacherService(repository=uow.teachers)
        self.student = StudentService(repository=uow.students)
        self.slot = SlotService(repository=uow.slots)
        self.lesson = LessonService(repository=uow.lessons)
        self.notification = NotificationService(repository=uow.notifications)
        self.statistics = StatisticsService(
            slot_repository=uow.slots,
            user_repository=uow.users,
        )
        self.recurrence = RecurrenceService(
            repository=uow.recurrences,
            slot_repository=uow.slots,
        )
        self.reschedule = RescheduleService(
            repository=uow.reschedules,
            slot_repository=uow.slots,
        )
        self.feedback = FeedbackService(
            repository=uow.feedback,
            slot_repository=uow.slots,
        )
