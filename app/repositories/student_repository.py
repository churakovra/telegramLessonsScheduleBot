from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from app.db.orm.user import User
from app.schemas.user_dto import UserDTO


class StudentRepository:
    def __init__(self, session: Session):
        self._db = session

    def _get_student(self, username: str) -> User | None:
        stmt = (
            select(User)
            .where(
                and_(
                    User.username == username,
                    User.is_student == True

                )
            )
        )
        student = self._db.scalar(stmt)
        return student

    def get_student(self, username: str) -> UserDTO | None:
        student = self._get_student(username)
        if student is None:
            return student
        return UserDTO.to_dto(student)