from sqlalchemy import select

from app.database import SessionLocal
from app.models.orm.teacher_students import TeacherStudents
from app.models.orm.teacher import Teacher
from app.models.orm.student import Student
from app.models.orm.admin import Admin
from app.models.orm.user import User

from app.models.orm.lesson_type import LessonType
from app.models.orm.lesson import Lesson

from app.models.user_dto import UserDTO


class TeacherRepo:
    @staticmethod
    async def attach_student(teacher: str, student: str) -> bool:
        try:
            with SessionLocal.begin() as session:
                teacher_student = TeacherStudents(teacher_username=teacher, student_username=student)
                session.add(teacher_student)
        except Exception:
            return False
        return True

    @staticmethod
    async def get_students(teacher: str) -> list[UserDTO]:
        users = list()
        stmt = (
            select(User)
            .join(TeacherStudents, User.username == TeacherStudents.student_username)
            .where(TeacherStudents.teacher_username == teacher)
        )
        with SessionLocal.begin() as session:
            res = session.execute(stmt)
            for index, row in enumerate(res):
                user = UserDTO.get_user_dto(row[index])
                users.append(user)
        return users
