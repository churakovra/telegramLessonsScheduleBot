import asyncio
from typing import Optional

from sqlalchemy import select
from sqlalchemy.util import await_only

from app.database import SessionLocal
from app.models.admin import Admin
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.user import User

from app.models.lesson_type import LessonType
from app.models.lesson import Lesson

from app.models.user_dto import UserDTO

async def get_user(username: str, session: Optional[SessionLocal]) -> User | UserDTO | None:
    stmt = (
        select(User)
        .where(User.username == username)
    )
    try:
        if session is not None:
            user = session.execute(stmt).first()
            result_user = user[0]
        else:
            with SessionLocal.begin() as session:
                user = session.execute(stmt).first()
                result_user = UserDTO.get_user_dto(user[0])
        return result_user
    except TypeError:
        return None
