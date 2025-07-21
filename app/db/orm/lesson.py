from typing import List
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.orm.base import Base
from app.db.orm.teacher_student import TeacherStudent
from app.db.orm.user import User


class Lesson(Base):
    __tablename__ = "lessons"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(nullable=False)
    duration: Mapped[int]
    uuid_teacher: Mapped[UUID] = mapped_column(ForeignKey("users.uuid"))
    price: Mapped[int]

    teacher: Mapped["User"] = relationship(argument="User", back_populates="lessons")
    lessons: Mapped[List["TeacherStudent"]] = relationship(argument="TeacherStudent", back_populates="lesson")
