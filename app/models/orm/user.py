from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.orm.base import Base

if TYPE_CHECKING:
    from app.models.orm.admin import Admin
    from app.models.orm.student import Student
    from app.models.orm.teacher import Teacher


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String)
    lastname: Mapped[str | None] = mapped_column(String)
    dt_reg: Mapped[datetime] = mapped_column(default=datetime.now)

    teacher: Mapped["Teacher"] = relationship(back_populates="user", uselist=False)
    student: Mapped["Student"] = relationship(back_populates="user", uselist=False)
    admin: Mapped["Admin"] = relationship(back_populates="user", uselist=False)
