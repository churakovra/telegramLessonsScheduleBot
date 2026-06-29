from uuid import UUID

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.orm.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import CreateUserDTO, UserDTO
from app.utils.enums.bot_values import UserRole


class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession, *, auto_commit: bool = True):
        super().__init__(session, auto_commit=auto_commit)

    async def add_user(self, user_dto: CreateUserDTO) -> UserDTO:
        user = User(**user_dto.model_dump(exclude="role"))
        return UserDTO.model_validate(await self.add(user))

    async def get_user(self, username: str) -> UserDTO | None:
        stmt = select(User).where(User.username == username)
        return await self.one_or_none_dto(stmt, UserDTO)

    async def get_admin_counts(self) -> tuple[int, int, int]:
        stmt = select(
            func.count(User.uuid),
            func.count().filter(User.is_teacher.is_(True)),
            func.count().filter(User.is_student.is_(True)),
        )
        total_users, total_teachers, total_students = (
            await self.session.execute(stmt)
        ).one()
        return int(total_users), int(total_teachers), int(total_students)

    async def edit_role(self, user_uuid: UUID, role: UserRole, status: bool) -> None:
        if role == UserRole.TEACHER:
            values = {"is_teacher": status}
        elif role == UserRole.ADMIN:
            values = {"is_admin": status}
        elif role == UserRole.STUDENT:
            values = {"is_student": status}
        else:
            raise ValueError(f"role {role} is unacceptable")

        stmt = update(User).where(User.uuid == user_uuid).values(**values)
        await self.execute(stmt)
        # TODO add log to db with initiator_user, dt of changing status etc

    async def delete_user(self, user_uuid: UUID) -> None:
        stmt = delete(User).where(User.uuid == user_uuid)
        await self.execute(stmt)
