from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.orm.lesson import Lesson
from app.db.orm.user import User
from app.utils.enums.bot_values import UserRoles
from app.schemas.user_dto import UserDTO


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._db = session

    async def add_user(self, user: UserDTO):
        user = User(**user.model_dump())
        self._db.add(user)
        await self._db.commit()
        await self._db.refresh(user)

    async def get_user(self, username: str) -> UserDTO | None:
        stmt = select(User).where(User.username == username)
        user = await self._db.scalar(stmt)
        if user is None:
            return user
        return UserDTO(
            uuid=user.uuid,
            username=user.username,
            firstname=user.firstname,
            lastname=user.lastname,
            is_student=user.is_student,
            is_teacher=user.is_teacher,
            is_admin=user.is_admin,
            chat_id=user.chat_id,
            dt_reg=user.dt_reg,
            dt_edit=user.dt_edit
        )

    async def edit_role(self, user_uuid: UUID, role: UserRoles, status: bool):
        if role == UserRoles.TEACHER:
            stmt = (
                update(User)
                .where(User.uuid == user_uuid)
                .values(
                    is_teacher=status,
                    dt_edit=datetime.now(timezone.utc).astimezone()
                )
            )
        elif role == UserRoles.ADMIN:
            stmt = (
                update(User)
                .where(User.uuid == user_uuid)
                .values(
                    is_admin=status,
                    dt_edit=datetime.now(timezone.utc).astimezone()
                )
            )
        elif role == UserRoles.STUDENT:
            stmt = (
                update(User)
                .where(User.uuid == user_uuid)
                .values(
                    is_student=status,
                    dt_edit=datetime.now(timezone.utc).astimezone()
                )
            )
        else:
            raise ValueError(f"role {role} is unacceptable")
        await self._db.execute(stmt)
        await self._db.commit()
        # TODO add log to db with initiator_user, dt of changing status etc
