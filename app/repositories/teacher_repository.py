from uuid import UUID

from sqlalchemy import select, and_, update, func, not_
from sqlalchemy.orm import Session

from app.db.orm.slot import Slot
from app.db.orm.teacher_students import TeacherStudents
from app.db.orm.user import User
from app.schemas.user_dto import UserDTO


class TeacherRepository:
    def __init__(self, session: Session):
        self._db = session

    def add_teacher(self, user_uuid: UUID):
        stmt = (
            update(User)
            .where(User.uuid == user_uuid)
            .values(is_student=False)
            .values(is_teacher=True)
        )
        self._db.execute(stmt)
        self._db.commit()

    def _get_teacher(self, username: str) -> User | None:
        stmt = (
            select(User)
            .where(
                and_(
                    User.username == username,
                    User.is_teacher == True

                )
            )
        )
        teacher = self._db.scalar(stmt)
        return teacher

    def get_teacher(self, username: str) -> UserDTO | None:
        teacher = self._get_teacher(username)
        if teacher is None:
            return teacher
        return UserDTO.to_dto(teacher)

    def remove_teacher(self, teacher_uuid: UUID):
        stmt = (
            update(User)
            .where(User.uuid == teacher_uuid)
            .values(is_teacher=False)
            .values(is_student=True)
        )
        self._db.execute(stmt)
        self._db.commit()

    def attach_student(self, teacher_uuid: UUID, student_uuid: UUID):
        teacher_student = TeacherStudents.new_instance(teacher_uuid, student_uuid)
        self._db.add(teacher_student)
        self._db.commit()
        self._db.refresh(teacher_student)
        return teacher_student.uuid

    def get_students(self, teacher_uuid: UUID) -> list[UserDTO]:
        users = list()
        stmt = (
            select(User)
            .join(TeacherStudents, User.uuid == TeacherStudents.uuid_student)
            .where(TeacherStudents.uuid_teacher == teacher_uuid)
        )
        for user in self._db.scalars(stmt):
            users.append(UserDTO.to_dto(user))

        return users

    def get_unsigned_students(self, teacher_uuid: UUID):
        users = list()
        ts_subquery = select(TeacherStudents.uuid_student).where(
            TeacherStudents.uuid_teacher == teacher_uuid).scalar_subquery()

        slots_subquery = select(Slot.uuid_student).where(Slot.dt_add > func.now()).scalar_subquery()
        stmt = (
            select(User)
            .where(
                and_(
                    User.uuid.in_(ts_subquery),
                    not_(User.uuid.in_(slots_subquery))
                )
            )
        )
        for user in self._db.scalars(stmt):
            users.append(UserDTO.to_dto(user))
        return users
