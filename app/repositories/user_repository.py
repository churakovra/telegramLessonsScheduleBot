from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.orm.lesson import Lesson
from app.database.orm.user import User
from app.utils.enums.bot_values import UserRole
from app.schemas.user_dto import CreateUserDTO, UserDTO


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._db = session

    async def add_user(self, user_dto: CreateUserDTO) -> User:
        user = User(**user_dto.model_dump(exclude="role"))
        self._db.add(user)
        await self._db.commit()
        await self._db.refresh(user)
        return user

    async def get_user(self, username: str) -> UserDTO | None:
        stmt = select(User).where(User.username == username)
        user = await self._db.scalar(stmt)
        if user is None:
            return user
        return UserDTO.model_validate(user)

    async def edit_role(self, user_uuid: UUID, role: UserRole, status: bool):
        if role == UserRole.TEACHER:
            stmt = update(User).where(User.uuid == user_uuid).values(is_teacher=status)
        elif role == UserRole.ADMIN:
            stmt = update(User).where(User.uuid == user_uuid).values(is_admin=status)
        elif role == UserRole.STUDENT:
            stmt = update(User).where(User.uuid == user_uuid).values(is_student=status)
        else:
            raise ValueError(f"role {role} is unacceptable")
        await self._db.execute(stmt)
        await self._db.commit()
        # TODO add log to db with initiator_user, dt of changing status etc

    async def delete_user(self, user_uuid: UUID):
        stmt = delete(User).where(User.uuid == user_uuid)
        await self._db.execute(stmt)
        await self._db.commit()
