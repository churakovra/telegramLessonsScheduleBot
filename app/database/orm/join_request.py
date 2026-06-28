from uuid import UUID, uuid4

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.orm.base import Base
from app.database.orm.user import User
from app.utils.enums.bot_values import JoinRequestStatus


class JoinRequest(Base):
    __tablename__ = "join_requests"

    uuid: Mapped[UUID] = mapped_column(Uuid(), default=uuid4, unique=True, nullable=False)
    student_uuid: Mapped[UUID] = mapped_column(
        ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False
    )
    teacher_uuid: Mapped[UUID] = mapped_column(
        ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[JoinRequestStatus] = mapped_column(
        SqlEnum(JoinRequestStatus, name="join_request_status"),
        default=JoinRequestStatus.PENDING,
        nullable=False,
    )

    student: Mapped["User"] = relationship(argument="User", foreign_keys=[student_uuid])
    teacher: Mapped["User"] = relationship(argument="User", foreign_keys=[teacher_uuid])

    __table_args__ = (
        UniqueConstraint(
            "student_uuid", "teacher_uuid", name="_join_request_student_teacher_uc"
        ),
    )
