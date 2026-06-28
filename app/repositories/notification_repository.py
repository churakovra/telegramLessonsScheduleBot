from datetime import datetime
from uuid import UUID

from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.orm.notification import Notification
from app.database.orm.slot import Slot
from app.database.orm.user import User
from app.repositories.base import BaseRepository
from app.schemas.notification import CreateNotificationDTO, NotificationDTO
from app.utils.enums.bot_values import NotificationTriggerType


class NotificationRepository(BaseRepository):
    def __init__(self, session: AsyncSession, *, auto_commit: bool = True):
        super().__init__(session, auto_commit=auto_commit)

    async def create_notification(
        self, notification_dto: CreateNotificationDTO
    ) -> NotificationDTO:
        notification = Notification(**notification_dto.model_dump())
        return NotificationDTO.model_validate(await self.add(notification))

    async def get_teacher_notifications(
        self, teacher_uuid: UUID
    ) -> list[NotificationDTO]:
        stmt = (
            select(Notification)
            .where(Notification.teacher_uuid == teacher_uuid)
            .order_by(Notification.created_at.desc())
        )
        return await self.list_dto(stmt, NotificationDTO)

    async def get_active_before_lesson_notifications(
        self,
    ) -> list[NotificationDTO]:
        stmt = select(Notification).where(
            and_(
                Notification.is_active.is_(True),
                Notification.trigger_type == NotificationTriggerType.BEFORE_LESSON,
            )
        )
        return await self.list_dto(stmt, NotificationDTO)

    async def delete_notification(self, notification_uuid: UUID) -> None:
        stmt = delete(Notification).where(Notification.uuid == notification_uuid)
        await self.execute(stmt)

    async def get_students_for_notification_window(
        self,
        teacher_uuid: UUID,
        start_at: datetime,
        end_at: datetime,
    ) -> list[tuple[int, datetime]]:
        stmt = (
            select(User.chat_id, Slot.dt_start)
            .join(Slot, Slot.uuid_student == User.uuid)
            .where(
                Slot.uuid_teacher == teacher_uuid,
                Slot.uuid_student.is_not(None),
                Slot.dt_start >= start_at,
                Slot.dt_start < end_at,
            )
        )
        return [(chat_id, dt_start) for chat_id, dt_start in await self.session.execute(stmt)]
