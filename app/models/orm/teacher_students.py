from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.orm.base import Base

if TYPE_CHECKING:
    from app.models.orm.student import Student
    from app.models.orm.teacher import Teacher


class TeacherStudents(Base):
    __tablename__ = "teacher_students"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    teacher_username: Mapped[str] = mapped_column(String, ForeignKey("teachers.username"))
    student_username: Mapped[str] = mapped_column(String, ForeignKey("students.username"))
    dt_apply: Mapped[datetime] = mapped_column(default=datetime.now)

    teacher: Mapped["Teacher"] = relationship(back_populates="teacher_students")
    student: Mapped["Student"] = relationship(back_populates="teacher_students")
