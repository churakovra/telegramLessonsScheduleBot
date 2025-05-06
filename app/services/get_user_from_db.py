from sqlalchemy import select

from app.database import SessionLocal
from app.models.admin import Admin
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.user import User

from app.models.lesson_type import LessonType
from app.models.lesson import Lesson


async def get_user(username: str, session: SessionLocal) -> User:
    stmt = select(User).where(User.username == username)
    user = session.execute(stmt).first()
    return user[0]
