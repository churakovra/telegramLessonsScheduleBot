from app.models.student import Student
from app.models.teacher import Teacher
from app.models.admin import Admin
from app.models.user import User
from app.database import SessionLocal


async def add_user(user: User):
    with SessionLocal.begin() as session:
        session.add(user)
        session.add(Student(user=user))
