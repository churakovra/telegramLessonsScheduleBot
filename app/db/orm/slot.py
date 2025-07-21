from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.orm.base import Base
from app.db.orm.user import User
from app.schemas.slot_dto import SlotDTO


class Slot(Base):
    __tablename__ = "slots"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    uuid_teacher: Mapped[UUID] = mapped_column(ForeignKey("users.uuid"), nullable=False)
    dt_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    dt_add: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    uuid_student: Mapped[UUID] = mapped_column(ForeignKey("users.uuid"), nullable=True)
    dt_spot: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint('uuid_teacher', 'dt_start', name='_teacher_dt_start_uc'),
    )

    teacher: Mapped["User"] = relationship(
        argument="User",
        foreign_keys=[uuid_teacher],
        back_populates="teacher_slots"
    )
    student: Mapped["User"] = relationship(
        argument="User",
        foreign_keys=[uuid_student],
        back_populates="student_slots"
    )

    @classmethod
    def new_instance(cls, slot_dto: SlotDTO):
        return cls(
            uuid=slot_dto.uuid,
            uuid_teacher=slot_dto.uuid_teacher,
            dt_start=slot_dto.dt_start,
            dt_add=slot_dto.dt_add,
            uuid_student=slot_dto.uuid_student,
            dt_spot=slot_dto.dt_spot
        )
