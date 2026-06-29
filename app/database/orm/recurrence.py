from datetime import date, time
from uuid import UUID

from sqlalchemy import Boolean, Date, ForeignKey, Integer, Time, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.orm.base import Base
from app.database.orm.user import User


class RecurrenceRule(Base):
    __tablename__ = "recurrence_rules"

    uuid: Mapped[UUID] = mapped_column(Uuid(), unique=True, nullable=False)
    teacher_uuid: Mapped[UUID] = mapped_column(
        ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False
    )
    day_of_week: Mapped[int] = mapped_column(Integer, nullable=False)
    time_start: Mapped[time] = mapped_column(Time(), nullable=False)
    time_end: Mapped[time] = mapped_column(Time(), nullable=False)
    slot_duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    date_start: Mapped[date] = mapped_column(Date(), nullable=False)
    date_end: Mapped[date] = mapped_column(Date(), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    teacher: Mapped["User"] = relationship(argument="User")
