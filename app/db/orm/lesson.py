from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.orm.base import Base

if TYPE_CHECKING:
    from app.db.orm.user import User


class Lesson(Base):
    __tablename__ = "lessons"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(nullable=False)
    duration: Mapped[float]
    uuid_teacher: Mapped[UUID] = mapped_column(ForeignKey("users.uuid"))
    price: Mapped[int]

    teacher: Mapped["User"] = relationship(back_populates="lessons")
