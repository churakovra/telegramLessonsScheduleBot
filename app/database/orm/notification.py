from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Integer, String, Uuid
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.orm.base import Base
from app.database.orm.user import User
from app.utils.enums.bot_values import NotificationTriggerType


class Notification(Base):
    __tablename__ = "notifications"

    uuid: Mapped[UUID] = mapped_column(Uuid(), unique=True, nullable=False)
    teacher_uuid: Mapped[UUID] = mapped_column(
        ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False
    )
    text: Mapped[str] = mapped_column(String, nullable=False)
    trigger_type: Mapped[NotificationTriggerType] = mapped_column(
        SqlEnum(NotificationTriggerType, name="notification_trigger_type"),
        nullable=False,
    )
    minutes_before: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    teacher: Mapped["User"] = relationship(argument="User")
