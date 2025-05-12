from app.models.orm.student import Student
from app.models.orm.user import User
from app.database import SessionLocal


async def add_user(user: User):
    with SessionLocal.begin() as session:
        session.add(user)
        session.add(Student(user=user))
