import asyncio

from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError

from app.database import SessionLocal
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.admin import Admin
from app.services.get_user_from_db import get_user
from app.utils.bot_values import BotValues as bv


async def change_user_status_in_db(initiator_user: str, teacher_username: str, new_status: bv.UserRoles) -> bool:
    try:
        with SessionLocal.begin() as session:
            delete_from_user_stmt = delete(Student).where(Student.username == teacher_username)

            session.execute(delete_from_user_stmt)
            user = await get_user(teacher_username, session)

            match new_status:
                case bv.UserRoles.TEACHER:
                    session.add(Teacher(user=user))
                case bv.UserRoles.ADMIN:
                    session.add(Admin(user=user))
                case bv.UserRoles.STUDENT:
                    session.add(Student(user=user))

    except IntegrityError:
        print(f"User {teacher_username} already exists at {new_status.name} table")
        return False
    return True

    # TODO add log to db with initiator_user, dt of changing status etc
