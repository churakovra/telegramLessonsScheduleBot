from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.lesson import Lesson


class LessonType(Base):
    __tablename__ = "lesson_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    duration: Mapped[float]

    lessons: Mapped[List["Lesson"]] = relationship(back_populates="lesson_type")