from typing import Optional

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError

from app.database import SessionLocal
from app.exceptions.user_exceptions import AddUserError
from app.models.orm.student import Student
from app.models.orm.teacher import Teacher
from app.models.orm.admin import Admin
from app.models.orm.user import User

from app.models.orm.lesson_type import LessonType
from app.models.orm.lesson import Lesson

from app.utils.bot_values import BotValues
from app.models.user_dto import UserDTO

roles = BotValues.UserRoles


class UserRepo:
    @staticmethod
    async def add_user(user: UserDTO):
        try:
            user_orm = User(
                username=user.username,
                firstname=user.firstname,
                lastname=user.lastname,
                chat_id=user.chat_id
            )
            with SessionLocal.begin() as session:
                session.add(user_orm)
                session.add(Student(user=user_orm))
        except IntegrityError:
            raise AddUserError

    @staticmethod
    async def get_user(username: str) -> UserDTO:
        stmt = select(User).where(User.username == username)
        try:
            with SessionLocal.begin() as session:
                user = session.execute(stmt).first()
                result_user = UserDTO.get_user_dto(user[0])
            return result_user
        except TypeError:
            raise GetUserError

    @staticmethod
    async def get_user_roles(username: str) -> list[roles]:
        stmt_admin = select(User.username).join(Admin).where(User.username == username)
        stmt_teacher = select(User.username).join(Teacher).where(User.username == username)
        stmt_student = select(User.username).join(Student).where(User.username == username)

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

    @staticmethod
    async def change_user_status_in_db(initiator_user: str, teacher_username: str, new_status: roles) -> bool:
        try:
            with SessionLocal.begin() as session:
                delete_from_user_stmt = delete(Student).where(Student.username == teacher_username)

                session.execute(delete_from_user_stmt)
                user = await UserRepo.get_user(teacher_username, session)

                match new_status:
                    case roles.TEACHER:
                        session.add(Teacher(user=user))
                    case roles.ADMIN:
                        session.add(Admin(user=user))
                    case roles.STUDENT:
                        session.add(Student(user=user))

        except IntegrityError:
            print(f"User {teacher_username} already exists at {new_status.name} table")
            return False
        return True
        # TODO add log to db with initiator_user, dt of changing status etc
