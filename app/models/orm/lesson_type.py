from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.orm.base import Base
from app.models.orm.lesson import Lesson


class LessonType(Base):
    __tablename__ = "lesson_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    duration: Mapped[float] = mapped_column()

    lessons: Mapped[List["Lesson"]] = relationship(back_populates="lesson_type")
