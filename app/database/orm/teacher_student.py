from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.orm.base import Base
from app.database.orm.user import User

if TYPE_CHECKING:
    from app.database.orm.lesson import Lesson


class TeacherStudent(Base):
    __tablename__ = "teacher_student"

    uuid_teacher: Mapped[UUID] = mapped_column(
        ForeignKey("users.uuid", ondelete="CASCADE")
    )
    uuid_student: Mapped[UUID] = mapped_column(
        ForeignKey("users.uuid", ondelete="CASCADE")
    )
    uuid_lesson: Mapped[UUID] = mapped_column(ForeignKey("lessons.uuid"), nullable=True)

    __table_args__ = (
        UniqueConstraint("uuid_teacher", "uuid_student", name="_teacher_student_uc"),
    )

    teacher: Mapped["User"] = relationship(
        argument="User",
        foreign_keys=[uuid_teacher],
        back_populates="teacher",
        passive_deletes=True,
    )
    student: Mapped["User"] = relationship(
        argument="User",
        foreign_keys=[uuid_student],
        back_populates="student",
        passive_deletes=True,
    )
    lesson: Mapped["Lesson"] = relationship(argument="Lesson", back_populates="lessons")
