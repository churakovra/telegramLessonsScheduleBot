from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.orm.base import Base
from app.db.orm.user import User


class Slot(Base):
    __tablename__ = "slots"

    id_teacher: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    dt_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    dt_add: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    id_student: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    dt_spot: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint("id_teacher", "dt_start", name="id_teacher_dt_start_uc"),
    )

    teacher: Mapped["User"] = relationship(
        argument="User", foreign_keys=[id_teacher], back_populates="teacher_slots"
    )
    student: Mapped["User"] = relationship(
        argument="User", foreign_keys=[id_student], back_populates="student_slots"
    )
