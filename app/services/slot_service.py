import string
from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.slot_repository import SlotRepository
from app.schemas.slot import CreateSlotDTO, SlotDTO
from app.utils.datetime_utils import WEEKDAYS
from app.utils.enums.bot_values import WeekFlag
from app.utils.exceptions.slot_exceptions import (
    SlotFreeNotFoundException,
    SlotNotFoundException,
    SlotsNotFoundException,
)
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class SlotService:
    def __init__(
        self,
        session: AsyncSession | None = None,
        repository: SlotRepository | None = None,
    ):
        if repository is None:
            if session is None:
                raise ValueError("SlotService requires session or repository")
            repository = SlotRepository(session)
        self._repository = repository

    async def add_slots(self, slots: list[CreateSlotDTO]):
        if not slots:
            return

        await self._repository.add_slots(slots)

    async def update_slots(self, slots: list[CreateSlotDTO], teacher_uuid: UUID):
        week = slots[0].dt_start.isocalendar().week
        existing_slots = await self._repository.get_slots(
            teacher_uuid=teacher_uuid, week=week
        )
        slots_dts = {slot.dt_start for slot in slots}
        existing_slots_dts = {
            existing_slot.dt_start for existing_slot in existing_slots
        }

        to_delete = existing_slots_dts - slots_dts
        to_add = slots_dts - existing_slots_dts

        slots_to_delete = [
            slot for slot in existing_slots if slot.dt_start in to_delete
        ]
        slots_to_add = [slot for slot in slots if slot.dt_start in to_add]

        await self._repository.delete_slots(slots=slots_to_delete)
        await self._repository.add_slots(slots_dto=slots_to_add)

    async def get_slot(self, slot_uuid: UUID) -> SlotDTO:
        slot = await self._repository.get_slot(slot_uuid)
        if slot is None:
            raise SlotNotFoundException(slot_uuid)
        return slot

    async def get_slots(self, teacher_uuid: UUID, week_flag: WeekFlag) -> list[SlotDTO]:
        week = datetime.now().isocalendar().week
        week = week + 1 if week_flag == WeekFlag.NEXT else week
        slots = await self._repository.get_slots(teacher_uuid, week)
        if len(slots) <= 0:
            raise SlotsNotFoundException(teacher_uuid, week_flag)
        return slots

    async def get_free_slots(self, teacher_uuid: UUID) -> list[SlotDTO]:
        slots = await self._repository.get_free_slots(teacher_uuid)
        if len(slots) <= 0:
            raise SlotFreeNotFoundException(teacher_uuid)
        return slots

    async def get_day_slots(self, day: datetime, teacher_uuid: UUID) -> list[SlotDTO]:
        slots = await self._repository.get_day_free_slots(day, teacher_uuid)
        if len(slots) <= 0:
            raise SlotFreeNotFoundException(teacher_uuid)
        return slots

    async def assign_slot(self, student_uuid: UUID, slot_uuid: UUID) -> SlotDTO:
        slot = await self.get_slot(slot_uuid)
        await self._repository.assign_slot(student_uuid, slot.uuid)
        return slot

    @staticmethod
    async def parse_slots(
        message_text: str, uuid_teacher: UUID, week_flag: WeekFlag
    ) -> list[CreateSlotDTO]:
        # Split message on day and time
        raw_mt = [word.strip(string.punctuation) for word in message_text.split()]
        slots = list[CreateSlotDTO]()
        days_delta = 0 if week_flag == WeekFlag.CURRENT else 7
        weekday_index = 0
        for word in raw_mt:
            try:
                # If word is Time -> create CreateSlotDTO, else raise ValueError
                time = datetime.strptime(word, "%H:%M")
                today = datetime.today()
                # Count slot's date
                slot_date = (
                    today + timedelta(days=days_delta - today.weekday() + weekday_index)
                ).date()
                slot_dt = datetime(
                    day=slot_date.day,
                    month=slot_date.month,
                    year=slot_date.year,
                    hour=time.hour,
                    minute=time.minute,
                )
                slots.append(
                    CreateSlotDTO(
                        uuid_teacher=uuid_teacher,
                        dt_start=slot_dt,
                        uuid_student=None,
                        dt_spot=None,
                    )
                )
            # Catch exception if str to date failed (row 64)
            except ValueError:
                # weekday_index using for count slot date on the next weeek
                for index, weekdays in WEEKDAYS.items():
                    if word in weekdays:
                        weekday_index = index
                        break

        return slots

    async def delete_slots_attached_to_student(self, student_uuid: UUID):
        await self._repository.delete_slots_attached_to_student(student_uuid)

    async def delete_slot(self, slot_uuid: UUID):
        await self._repository.delete_slot(slot_uuid)
