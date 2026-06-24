from collections.abc import Iterable
from typing import Any, TypeVar

from pydantic import BaseModel
from sqlalchemy import Delete, Select, Update
from sqlalchemy.ext.asyncio import AsyncSession

InstanceT = TypeVar("InstanceT")
DtoT = TypeVar("DtoT", bound=BaseModel)


class BaseRepository:
    def __init__(self, session: AsyncSession, *, auto_commit: bool = True):
        self.session = session
        self.auto_commit = auto_commit

    async def add(self, instance: InstanceT) -> InstanceT:
        self.session.add(instance)
        await self.session.flush()
        if self.auto_commit:
            await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def add_many(self, instances: Iterable[InstanceT]) -> None:
        instances = list(instances)
        if not instances:
            return

        self.session.add_all(instances)
        await self.session.flush()
        if self.auto_commit:
            await self.session.commit()

    async def execute(self, stmt: Update | Delete) -> None:
        await self.session.execute(stmt)
        await self.session.flush()
        if self.auto_commit:
            await self.session.commit()

    async def scalar(self, stmt: Select[Any]) -> Any | None:
        return await self.session.scalar(stmt)

    async def scalars(self, stmt: Select[Any]) -> list[Any]:
        return list(await self.session.scalars(stmt))

    async def one_or_none_dto(
        self, stmt: Select[Any], dto_cls: type[DtoT]
    ) -> DtoT | None:
        instance = await self.scalar(stmt)
        if instance is None:
            return None
        return dto_cls.model_validate(instance)

    async def list_dto(self, stmt: Select[Any], dto_cls: type[DtoT]) -> list[DtoT]:
        return [
            dto_cls.model_validate(instance) for instance in await self.scalars(stmt)
        ]
