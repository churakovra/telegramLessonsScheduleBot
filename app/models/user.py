from datetime import datetime
from typing import Optional

from sqlalchemy import String, DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.teacher import Teacher


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    firstname: Mapped[str] = mapped_column(Optional[str])
    lastname: Mapped[str] = mapped_column(Optional[str])
    dt_reg: Mapped[datetime] = mapped_column(DATETIME)

    teacher: Mapped[Teacher] = relationship(back_populates="username")
    student: Mapped[Student] = relationship(back_populates="username")
    admin: Mapped[Admin] = relationship(back_populates="username")
