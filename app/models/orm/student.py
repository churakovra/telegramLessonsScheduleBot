from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.orm.base import Base
from app.models.orm.lesson import Lesson
from app.models.orm.teacher_students import TeacherStudents
from app.models.orm.user import User


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, ForeignKey("users.username"), nullable=False, unique=True)
    notifications: Mapped[bool] = mapped_column(default=True)

    user: Mapped["User"] = relationship(back_populates="student")
    lessons: Mapped[list["Lesson"]] = relationship(back_populates="student")
    teacher_students: Mapped["TeacherStudents"] = relationship(back_populates="student")
