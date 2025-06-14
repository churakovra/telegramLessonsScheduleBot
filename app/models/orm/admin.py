from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.orm.base import Base
from app.models.orm.user import User


class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, ForeignKey("users.username"), nullable=False)
    notifications: Mapped[bool] = mapped_column(default=True)

    user: Mapped[User] = relationship(back_populates="admin")
