from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions.user_exceptions import UserNotFoundException
from app.handlers.commands.new_slots import UserRoles
from app.repositories.teacher_repository import TeacherRepository
from app.schemas.user_dto import UserDTO


class TeacherService:
    def __init__(self, session: Session):
        self._repository = TeacherRepository(session)

    def get_teacher(self, username: str) -> UserDTO:
        teacher = self._repository.get_teacher(username)
        if teacher is None:
            raise UserNotFoundException(UserRoles.TEACHER, username)
        return teacher

    def attach_student(self, *, teacher_uuid: UUID, student_uuid: UUID):
        self._repository.attach_student(teacher_uuid, student_uuid)

    def get_students(self, teacher_uuid: UUID) -> list[UserDTO]:
        return self._repository.get_students(teacher_uuid)
