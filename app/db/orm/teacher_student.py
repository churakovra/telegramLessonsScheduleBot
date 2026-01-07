import uuid
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.orm.base import Base
from app.db.orm.user import User

if TYPE_CHECKING:
    from app.db.orm.lesson import Lesson


class TeacherStudent(Base):
    __tablename__ = "teacher_student"

    id_teacher: Mapped[int] = mapped_column(ForeignKey("users.id"))
    id_student: Mapped[int] = mapped_column(ForeignKey("users.id"))
    id_lesson: Mapped[int] = mapped_column(
        ForeignKey("lessons.id", ondelete="CASCADE"), nullable=True
    )

    __table_args__ = (
        UniqueConstraint("id_teacher", "id_student", name="id_teacher_student_uc"),
    )

    teacher: Mapped["User"] = relationship(
        argument="User", foreign_keys=[id_teacher], back_populates="teacher"
    )
    student: Mapped["User"] = relationship(
        argument="User", foreign_keys=[id_student], back_populates="student"
    )
    lesson: Mapped["Lesson"] = relationship(argument="Lesson", back_populates="lessons")
