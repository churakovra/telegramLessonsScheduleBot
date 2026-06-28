from uuid import UUID

from sqlalchemy import ForeignKey, Integer, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.orm.base import Base
from app.database.orm.slot import Slot
from app.database.orm.user import User


class Feedback(Base):
    __tablename__ = "feedback"

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
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text(), nullable=True)

    __table_args__ = (UniqueConstraint("slot_uuid", name="_feedback_slot_uc"),)

    slot: Mapped["Slot"] = relationship(argument="Slot")
    student: Mapped["User"] = relationship(argument="User", foreign_keys=[student_uuid])
    teacher: Mapped["User"] = relationship(argument="User", foreign_keys=[teacher_uuid])
