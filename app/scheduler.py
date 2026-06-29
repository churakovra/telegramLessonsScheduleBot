import asyncio
from contextlib import suppress

from app.database.database import async_session_factory
from app.database.unit_of_work import UnitOfWork
from app.keyboard.fabric import feedback_rating_menu
from app.message.models import BotMessage, MessageRecipient
from app.notifier.sender import MessageSender
from app.services.container import Services
from app.utils.bot_strings import BotStrings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class NotificationScheduler:
    def __init__(self, sender: MessageSender, interval_seconds: int = 60) -> None:
        self.sender = sender
        self.interval_seconds = interval_seconds
        self._task: asyncio.Task | None = None

    def start(self) -> None:
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self._run())
            logger.info("NotificationScheduler has been started")

    async def stop(self) -> None:
        if self._task is None:
            return
        self._task.cancel()
        with suppress(asyncio.CancelledError):
            await self._task
        logger.info("NotificationScheduler has been stopped")

    async def _run(self) -> None:
        while True:
            try:
                async with async_session_factory() as session:
                    uow = UnitOfWork(session)
                    services = Services(uow)
                    await services.recurrence.materialize_slots()
                    await services.notification.check_and_send_notifications(
                        sender=self.sender
                    )
                    await self._send_feedback_prompts(services)
                    await uow.commit()
            except Exception:
                logger.warning(
                    "Notification scheduler tick failed; retrying on next tick",
                    exc_info=True,
                )
            await asyncio.sleep(self.interval_seconds)

    async def _send_feedback_prompts(self, services: Services) -> None:
        prompts = await services.feedback.get_slots_waiting_feedback_prompt()
        for prompt in prompts:
            try:
                await self.sender.send(
                    message=BotMessage(
                        text=BotStrings.Student.FEEDBACK_PROMPT,
                        markup=feedback_rating_menu(slot_uuid=prompt.slot_uuid),
                    ),
                    recipients=[MessageRecipient(chat_id=prompt.student_chat_id)],
                )
                await services.feedback.mark_feedback_prompt_sent(prompt.slot_uuid)
            except Exception:
                logger.warning(
                    "Failed to send feedback prompt for slot %s",
                    prompt.slot_uuid,
                    exc_info=True,
                )
