from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.services.container import Services
from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        services: Services = data["services"]
        username = self.get_username(event)
        if username is None:
            return await handler(event, data)

        try:
            user = await services.user.get_user(username)
            data["user"] = user
        except UserNotFoundException:
            # TODO send on_error event in NotificationService via rmq
            pass
        return await handler(event, data)

    @staticmethod
    def get_username(event: TelegramObject) -> str | None:
        event_type = event.message if event.message else event.callback_query  # type: ignore[attr-defined]
        if not event_type or not event_type.from_user:
            return None
        return event_type.from_user.username
