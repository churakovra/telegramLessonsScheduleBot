from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.lesson_repository import LessonRepository
from app.repositories.slot_repository import SlotRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.teacher_repository import TeacherRepository
from app.repositories.user_repository import UserRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepository(session, auto_commit=False)
        self.teachers = TeacherRepository(session, auto_commit=False)
        self.students = StudentRepository(session, auto_commit=False)
        self.slots = SlotRepository(session, auto_commit=False)
        self.lessons = LessonRepository(session, auto_commit=False)

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
