from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.orm.base import Base
from app.database.orm.user import User


class Slot(Base):
    __tablename__ = "slots"

    uuid: Mapped[UUID] = mapped_column(Uuid(), unique=True)
    uuid_teacher: Mapped[int] = mapped_column(ForeignKey("users.uuid"), nullable=False)
    dt_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    dt_add: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    uuid_student: Mapped[int] = mapped_column(ForeignKey("users.uuid"), nullable=True)
    dt_spot: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint("uuid_teacher", "dt_start", name="_teacher_dt_start_uc"),
    )

    teacher: Mapped["User"] = relationship(
        argument="User", foreign_keys=[uuid_teacher], back_populates="teacher_slots"
    )
    student: Mapped["User"] = relationship(
        argument="User", foreign_keys=[uuid_student], back_populates="student_slots"
    )
