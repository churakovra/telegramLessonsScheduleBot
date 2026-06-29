from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.notifier.sender import MessageSender


class SenderInjectionMiddleware(BaseMiddleware):
    """Middleware that injects MessageSender into handler kwargs."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        dispatcher = data.get("dispatcher")
        if dispatcher:
            sender = getattr(dispatcher, "sender", None)
            if isinstance(sender, MessageSender):
                data["sender"] = sender
            else:
                # Fallback: create a sender with bot from context
                bot = data.get("bot")
                if bot is not None:
                    data["sender"] = MessageSender(bot=bot)
        return await handler(event, data)
