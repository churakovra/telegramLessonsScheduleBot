from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from app.db.orm.user import User
from app.schemas.student_dto import StudentDTO


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

    def get_student(self, username: str) -> StudentDTO | None:
        student = self._get_student(username)
        if student is None:
            return student
        return StudentDTO(
            uuid=student.uuid,
            username=student.username,
            firstname=student.firstname,
            lastname=student.lastname,
            is_student=student.is_student,
            is_teacher=student.is_teacher,
            is_admin=student.is_admin,
            chat_id=student.chat_id,
            dt_reg=student.dt_reg,
            dt_edit=student.dt_edit
        )
