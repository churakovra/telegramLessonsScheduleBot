from sqlalchemy import select

from app.database import SessionLocal
from app.models.orm.admin import Admin
from app.models.orm.student import Student
from app.models.orm.teacher import Teacher
from app.models.orm.user import User

from app.utils.bot_values import BotValues

roles = BotValues.UserRoles

async def get_user_status(username: str) -> list[roles]:
    stmt_admin = select(User.username).join(Admin).where(User.username==username)
    stmt_teacher = select(User.username).join(Teacher).where(User.username==username)
    stmt_student = select(User.username).join(Student).where(User.username==username)

    stmts = {
        roles.ADMIN: stmt_admin,
        roles.TEACHER: stmt_teacher,
        roles.STUDENT: stmt_student,
    }

    res = []

    with SessionLocal.begin() as session:
        for role, stmt in stmts.items():
            status = session.execute(stmt).first()
            if status is not None:
                res.append(role)

        if len(res) > 0:
            return res
        return [roles.NOT_DEFINED]
