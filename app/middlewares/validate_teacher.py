from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from app.database.database import async_session_factory
from app.services.teacher_service import TeacherService
from app.utils.bot_strings import BotStrings
from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class ValidateTeacherMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ):
        if not isinstance(event, (Message, CallbackQuery)):
            return handler(event, data)
        async with async_session_factory() as session:
            teacher_service = TeacherService(session)
            try:
                teacher = await teacher_service.get_teacher(event.from_user.username)
                return await handler(event, data)
            except UserNotFoundException:
                logger.error(
                    f"Teacher {teacher.uuid} tried to add new lesson, but didn't have enough rights"
                )
                await event.message.answer(BotStrings.Teacher.NOT_ENOUGH_RIGHTS)
                return
