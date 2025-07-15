from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.orm.base import Base
from app.db.orm.user import User

if TYPE_CHECKING:
    from app.db.orm.lesson import Lesson


class TeacherStudent(Base):
    __tablename__ = "teacher_student"

    uuid_teacher: Mapped[UUID] = mapped_column(ForeignKey("users.uuid"))
    uuid_student: Mapped[UUID] = mapped_column(ForeignKey("users.uuid"))
    uuid_lesson: Mapped[UUID] = mapped_column(ForeignKey("lessons.uuid"))

    __table_args__ = (
        PrimaryKeyConstraint("uuid_teacher", "uuid_student", "uuid_lesson"),
    )

    teacher: Mapped["User"] = relationship(
        argument="User",
        foreign_keys=[uuid_teacher],
        back_populates="teacher"
    )
    student: Mapped["User"] = relationship(
        argument="User",
        foreign_keys=[uuid_student],
        back_populates="student"
    )
    lesson: Mapped["Lesson"] = relationship(
        argument="Lesson",
        back_populates="lessons"
    )

    @classmethod
    def new_instance(cls, uuid_teacher: UUID, uuid_student: UUID):
        return cls(
            uuid=uuid4(),
            uuid_teacher=uuid_teacher,
            uuid_student=uuid_student
        )
