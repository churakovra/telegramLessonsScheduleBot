from sqlalchemy import select

from app.database import SessionLocal
from app.models.admin import Admin
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.user import User

from app.models.lesson_type import LessonType
from app.models.lesson import Lesson

from app.utils.bot_values import BotValues as bv


async def get_user_status(username: str) -> bv.UserRoles:
    stmt_admin = select(User.username).join(Admin).where(User.username==username)
    stmt_teacher = select(User.username).join(Teacher).where(User.username==username)
    stmt_student = select(User.username).join(Student).where(User.username==username)

    stmts = {
        bv.UserRoles.ADMIN: stmt_admin,
        bv.UserRoles.TEACHER: stmt_teacher,
        bv.UserRoles.STUDENT: stmt_student,
    }

    with SessionLocal.begin() as session:
        for role, stmt in stmts.items():
            status = session.execute(stmt).first()
            if status is not None:
                return role
        return bv.UserRoles.NOT_DEFINED
