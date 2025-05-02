from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from lesson_type import LessonType
    from student import Student
    from teacher import Teacher


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    id_teacher: Mapped[int] = mapped_column(ForeignKey("teachers.id"), nullable=False)
    id_student: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    id_lesson_type: Mapped[int] = mapped_column(ForeignKey("lesson_types.id"), nullable=False)
    dt_start: Mapped[datetime] = mapped_column(nullable=False)

    teacher: Mapped["Teacher"] = relationship(back_populates="lessons")
    student: Mapped["Student"] = relationship(back_populates="lessons")
    lesson_type: Mapped["LessonType"] = relationship(back_populates="lessons")
