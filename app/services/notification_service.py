from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.message.models import BotMessage, MessageRecipient
from app.notifier.sender import MessageSender
from app.repositories.notification_repository import NotificationRepository
from app.schemas.notification import CreateNotificationDTO, NotificationDTO
from app.utils.enums.bot_values import NotificationTriggerType
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class NotificationService:
    def __init__(
        self,
        session: AsyncSession | None = None,
        repository: NotificationRepository | None = None,
    ):
        if repository is None:
            if session is None:
                raise ValueError("NotificationService requires session or repository")
            repository = NotificationRepository(session)
        self._repository = repository

    async def create_notification(
        self,
        teacher_uuid: UUID,
        text: str,
        trigger_type: NotificationTriggerType,
        minutes_before: int,
    ) -> NotificationDTO:
        notification = CreateNotificationDTO(
            teacher_uuid=teacher_uuid,
            text=text,
            trigger_type=trigger_type,
            minutes_before=minutes_before,
        )
        return await self._repository.create_notification(notification)

    async def get_teacher_notifications(
        self, teacher_uuid: UUID
    ) -> list[NotificationDTO]:
        return await self._repository.get_teacher_notifications(teacher_uuid)

    async def delete_notification(self, notification_uuid: UUID) -> None:
        await self._repository.delete_notification(notification_uuid)

    async def check_and_send_notifications(self, sender: MessageSender) -> None:
        notifications = await self._repository.get_active_before_lesson_notifications()
        now = datetime.now(UTC).astimezone()

        for notification in notifications:
            start_at = now + timedelta(minutes=notification.minutes_before)
            end_at = start_at + timedelta(seconds=60)
            recipients = await self._repository.get_students_for_notification_window(
                teacher_uuid=notification.teacher_uuid,
                start_at=start_at,
                end_at=end_at,
            )
            if not recipients:
                continue

            try:
                await sender.send(
                    message=BotMessage(text=notification.text),
                    recipients=[
                        MessageRecipient(chat_id=chat_id)
                        for chat_id, _dt_start in recipients
                    ],
                )
            except Exception:
                logger.warning(
                    "Failed to send notification %s; will retry on next scheduler tick",
                    notification.uuid,
                    exc_info=True,
                )
