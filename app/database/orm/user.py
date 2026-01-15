from datetime import datetime
from typing import TYPE_CHECKING, List
from uuid import UUID, uuid4

from sqlalchemy import BigInteger, DateTime, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.orm.base import Base

if TYPE_CHECKING:
    from app.database.orm.lesson import Lesson
    from app.database.orm.slot import Slot
    from app.database.orm.teacher_student import TeacherStudent


class User(Base):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(Uuid(), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String, nullable=False)
    lastname: Mapped[str] = mapped_column(String, nullable=True)
    is_student: Mapped[bool] = mapped_column(default=True)
    is_teacher: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    chat_id: Mapped[int] = mapped_column(BigInteger)


    lessons: Mapped[list["Lesson"]] = relationship(argument="Lesson", back_populates="teacher")
    teacher_slots: Mapped[list["Slot"]] = relationship(argument="Slot", foreign_keys="[Slot.uuid_teacher]", back_populates="teacher")
    student_slots: Mapped[list["Slot"]] = relationship(argument="Slot", foreign_keys="[Slot.uuid_student]", back_populates="student")
    teacher: Mapped[list["TeacherStudent"]] = relationship(argument="TeacherStudent", foreign_keys="[TeacherStudent.uuid_teacher]", back_populates="teacher")
    student: Mapped[list["TeacherStudent"]] = relationship(argument="TeacherStudent", foreign_keys="[TeacherStudent.uuid_student]", back_populates="student")
