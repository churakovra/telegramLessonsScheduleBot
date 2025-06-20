from sqlalchemy.orm import Session

from app.exceptions.user_exceptions import UserNotFoundException
from app.handlers.commands.new_slots import UserRoles
from app.repositories.student_repository import StudentRepository
from app.schemas.user_dto import UserDTO


class StudentService:
    def __init__(self, session: Session):
        self._repository = StudentRepository(session)

    def get_student(self, username: str) -> UserDTO:
        student = self._repository.get_student(username)
        if student is None:
            raise UserNotFoundException(UserRoles.STUDENT, username)
        return student
