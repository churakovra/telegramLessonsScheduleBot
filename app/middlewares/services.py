from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.database.unit_of_work import UnitOfWork
from app.services.container import Services


class ServicesMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        uow: UnitOfWork = data["uow"]
        data["services"] = Services(uow)
        return await handler(event, data)
