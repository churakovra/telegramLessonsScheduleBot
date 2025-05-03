from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.lesson import Lesson
from app.models.user import User


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, ForeignKey("users.username"), nullable=False)
    notifications: Mapped[bool] = mapped_column(default=True)

    user: Mapped["User"] = relationship(back_populates="teacher")
    lessons: Mapped[list["Lesson"]] = relationship(back_populates="teacher")
