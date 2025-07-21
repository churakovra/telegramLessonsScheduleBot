from datetime import datetime
from typing import List, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.orm.base import Base

if TYPE_CHECKING:
    from app.db.orm.lesson import Lesson
    from app.db.orm.slot import Slot
    from app.db.orm.teacher_student import TeacherStudent


class User(Base):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String, nullable=False)
    lastname: Mapped[str] = mapped_column(String, nullable=True)
    is_student: Mapped[bool] = mapped_column(default=True)
    is_teacher: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    chat_id: Mapped[int] = mapped_column(BigInteger)
    dt_reg: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    dt_edit: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    lessons: Mapped[List["Lesson"]] = relationship(
        argument="Lesson",
        back_populates="teacher"
    )

    teacher_slots: Mapped[List["Slot"]] = relationship(
        argument="Slot",
        foreign_keys="[Slot.uuid_teacher]",
        back_populates="teacher"
    )
    student_slots: Mapped[List["Slot"]] = relationship(
        argument="Slot",
        foreign_keys="[Slot.uuid_student]",
        back_populates="student"
    )
    teacher: Mapped[List["TeacherStudent"]] = relationship(
        argument="TeacherStudent",
        foreign_keys="[TeacherStudent.uuid_teacher]",
        back_populates="teacher"
    )
    student: Mapped[List["TeacherStudent"]] = relationship(
        argument="TeacherStudent",
        foreign_keys="[TeacherStudent.uuid_student]",
        back_populates="student"
    )
