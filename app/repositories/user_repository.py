from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db.orm.user import User
from app.enums.bot_values import UserRoles
from app.schemas.user_dto import UserDTO


class UserRepository:
    def __init__(self, session: Session):
        self._db = session

    def add_user(self, user: UserDTO):
        user = User.from_dto(user)
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)

    async def get_user(self, username: str) -> UserDTO | None:
        stmt = select(User).where(User.username == username)
        user = self._db.scalar(stmt)
        if user is None:
            return user
        return UserDTO.to_dto(user)

    async def get_user_roles(self, username: str) -> list[roles]:
        stmt_admin = select(User.username).join(Admin).where(User.username == username)
        stmt_teacher = select(User.username).join(Teacher).where(User.username == username)
        stmt_student = select(User.username).join(Student).where(User.username == username)

        stmts = {
            roles.ADMIN: stmt_admin,
            roles.TEACHER: stmt_teacher,
            roles.STUDENT: stmt_student,
        }

        res = []

        for role, stmt in stmts.items():
            status = await self.db.scalar(stmt)
            if status is not None:
                res.append(role)

        if len(res) > 0:
            return res
        return [roles.NOT_DEFINED]

    async def change_user_status_in_db(self, initiator_user: str, teacher_username: str, new_status: roles) -> bool:

        delete_from_student_stmt = delete(Student).where(Student.username == teacher_username)
        await self.db.execute(delete_from_student_stmt)

        match new_status:
            case roles.TEACHER:
                self.db.add(Teacher(username=teacher_username))
            case roles.ADMIN:
                self.db.add(Admin(username=teacher_username))
            case roles.STUDENT:
                self.db.add(Student(username=teacher_username))

        return True
        # TODO add log to db with initiator_user, dt of changing status etc
