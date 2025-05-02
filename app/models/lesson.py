from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.lesson_type import LessonType
from app.models.student import Student
from app.models.teacher import Teacher


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_teacher = mapped_column(ForeignKey("teachers.id"))
    id_student = mapped_column(ForeignKey("students.id"))
    id_lesson_type = mapped_column(ForeignKey("lesson_types.id"))

    teacher: Mapped[Teacher] = relationship(back_populates="lessons")
    student: Mapped[Student] = relationship(back_populates="lessons")
    lesson_type: Mapped[LessonType] = relationship(back_populates="lessons")
