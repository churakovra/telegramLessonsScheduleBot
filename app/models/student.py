from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.user import User


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    username = mapped_column(ForeignKey("users.username"))
    notifications: Mapped[bool]

    user: Mapped[User] = relationship(back_populates="username")