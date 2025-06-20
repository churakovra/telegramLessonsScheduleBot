from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column

from app.db.orm.base import Base


class TeacherStudents(Base):
    __tablename__ = "teacher_students"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    uuid_teacher: Mapped[UUID]
    uuid_student: Mapped[UUID]

    @classmethod
    def new_instance(cls, uuid_teacher: UUID, uuid_student: UUID):
        return cls(
            uuid=uuid4(),
            uuid_teacher=uuid_teacher,
            uuid_student=uuid_student
        )
