from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.orm.base import Base

if TYPE_CHECKING:
    from app.db.orm.user import User
    from app.db.orm.lesson import Lesson


class Slot(Base):
    __tablename__ = "slots"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    uuid_teacher: Mapped[UUID] = mapped_column(ForeignKey("users.uuid"))
    uuid_lesson: Mapped[UUID] = mapped_column(ForeignKey("lessons.uuid"))
    dt_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    dt_add: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    uuid_student: Mapped[UUID] = mapped_column(ForeignKey("users.uuid"), nullable=True)
    dt_spot: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    teacher: Mapped["User"] = relationship(back_populates="slots")
    lesson: Mapped["Lesson"] = relationship(back_populates="slots")
