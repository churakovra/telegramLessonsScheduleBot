from app.database.unit_of_work import UnitOfWork
from app.services.lesson_service import LessonService
from app.services.slot_service import SlotService
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
