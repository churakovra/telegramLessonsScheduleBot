from uuid import UUID
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.orm.base import Base

if TYPE_CHECKING:
    from lesson_type import LessonType
    from student import Student
    from teacher import Teacher


class Lesson(Base):
    __tablename__ = "lessons"

    uuid_slot: Mapped[UUID] = mapped_column(primary_key=True)
    uuid_day: Mapped[UUID] = mapped_column(primary_key=True)
    t_username: Mapped[str] = mapped_column(ForeignKey("teachers.username"), nullable=False)
    s_username: Mapped[str] = mapped_column(ForeignKey("students.username"), nullable=True)
    id_lesson_type: Mapped[int] = mapped_column(ForeignKey("lesson_types.id"), nullable=True)
    dt_start: Mapped[datetime] = mapped_column(nullable=False)
    dt_add: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    dt_spot: Mapped[datetime] = mapped_column(nullable=True)

    teacher: Mapped["Teacher"] = relationship(back_populates="lessons")
    student: Mapped["Student"] = relationship(back_populates="lessons")
    lesson_type: Mapped["LessonType"] = relationship(back_populates="lessons")
