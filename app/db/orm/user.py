from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import String, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.orm.base import Base
from app.db.orm.lesson import Lesson
from app.db.orm.slot import Slot


class User(Base):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String, nullable=False)
    lastname: Mapped[str]
    is_student: Mapped[bool] = mapped_column(default=True)
    is_teacher: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    chat_id: Mapped[int] = mapped_column(BigInteger)
    dt_reg: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    dt_edit: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    lessons: Mapped[List["Lesson"]] = relationship(back_populates="teacher")
    slots: Mapped[List["Slot"]] = relationship(back_populates="teacher")
