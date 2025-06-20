from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import String, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.orm.base import Base
from app.db.orm.lesson import Lesson
from app.db.orm.slot import Slot
from app.schemas.user_dto import UserDTO


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

    @classmethod
    def from_dto(cls, user: UserDTO):
        return cls(
            uuid=user.uuid,
            username=user.username,
            firstname=user.firstname,
            lastname=user.lastname,
            is_student=user.is_student,
            is_teacher=user.is_teacher,
            is_admin=user.is_admin,
            chat_id=user.chat_id,
            dt_reg=user.dt_reg,
            dt_edit=user.dt_edit
        )
