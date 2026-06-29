from datetime import date, time
from uuid import UUID

from sqlalchemy import Date, ForeignKey, Time, Uuid
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.orm.base import Base
from app.database.orm.slot import Slot
from app.database.orm.user import User
from app.utils.enums.bot_values import RescheduleStatus


class RescheduleRequest(Base):
    __tablename__ = "reschedule_requests"

    uuid: Mapped[UUID] = mapped_column(Uuid(), unique=True, nullable=False)
    slot_uuid: Mapped[UUID] = mapped_column(
        ForeignKey("slots.uuid", ondelete="CASCADE"), nullable=False
    )
    student_uuid: Mapped[UUID] = mapped_column(
        ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False
    )
    teacher_uuid: Mapped[UUID] = mapped_column(
        ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False
    )
    requested_date: Mapped[date] = mapped_column(Date(), nullable=False)
    requested_time: Mapped[time] = mapped_column(Time(), nullable=False)
    status: Mapped[RescheduleStatus] = mapped_column(
        SqlEnum(RescheduleStatus, name="reschedule_status"), nullable=False
    )

    slot: Mapped["Slot"] = relationship(argument="Slot")
    student: Mapped["User"] = relationship(argument="User", foreign_keys=[student_uuid])
    teacher: Mapped["User"] = relationship(argument="User", foreign_keys=[teacher_uuid])
