import calendar
import string
from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.slot_repository import SlotRepository
from app.schemas.slot_dto import SlotDTO
from app.utils.config.logger import setup_logger
from app.utils.datetime_utils import WEEKDAYS
from app.utils.exceptions.slot_exceptions import (
    SlotFreeNotFoundException,
    SlotNotFoundException,
)

logger = setup_logger("SlotService")


class SlotService:
    def __init__(self, session: AsyncSession):
        self._repository = SlotRepository(session)

    async def add_slots(self, slots: list[SlotDTO]):
        for slot in slots:
            try:
                await self._repository.add_slot(slot)
            except ValueError as e:
                logger.error(e)
                pass

    async def get_slot(self, slot_uuid: UUID) -> SlotDTO:
        slot = await self._repository.get_slot(slot_uuid)
        if slot is None:
            raise SlotNotFoundException(slot_uuid)
        return slot

    async def get_free_slots(self, teacher_uuid: UUID) -> list[SlotDTO]:
        slots = await self._repository.get_free_slots(teacher_uuid)
        if len(slots) <= 0:
            raise SlotFreeNotFoundException(teacher_uuid)
        return slots

    async def get_day_slots(self, day: datetime, teacher_uuid: UUID) -> list[SlotDTO]:
        slots = await self._repository.get_day_slots(day, teacher_uuid)
        if len(slots) <= 0:
            raise SlotFreeNotFoundException(teacher_uuid)
        return slots

    async def assign_slot(self, student_uuid: UUID, slot_uuid: UUID) -> SlotDTO:
        slot = await self.get_slot(slot_uuid)
        await self._repository.assign_slot(student_uuid, slot.uuid)
        return slot

    @staticmethod
    async def parse_slots(message_text: str, uuid_teacher: UUID) -> list[SlotDTO]:
        raw_mt = [
            word.strip(string.punctuation) for word in message_text.split()
        ]  # разбиваем сообщение на День и Время
        slots = list[SlotDTO]()
        weekday_index = None
        for word in raw_mt:
            try:
                time = datetime.strptime(
                    word, "%H:%M"
                )  # Если word - время, то создаем SlotDTO, иначе кидается ошибка
                today = datetime.today()
                slot_date = (
                    today + timedelta(days=7 - today.weekday() + weekday_index)
                ).date()  # Считаем дату слота
                slot_dt = datetime(
                    day=slot_date.day,
                    month=slot_date.month,
                    year=slot_date.year,
                    hour=time.hour,
                    minute=time.minute,
                )
                slots.append(
                    SlotDTO.new_dto(
                        uuid_teacher=uuid_teacher,
                        dt_start=slot_dt,
                        uuid_student=None,
                        dt_spot=None,
                    )
                )
            except (
                ValueError
            ):  # Ловим ошибку, если приведение строки к дате не получилось
                for (
                    index,
                    weekdays,
                ) in (
                    WEEKDAYS.items()
                ):  # weekday_index нужен для расчета даты слота на следующей неделе
                    if word in weekdays:
                        weekday_index = index
                        break

        return slots

    @staticmethod
    async def get_slot_reply(slots: list[SlotDTO]) -> str:
        response = ""
        slots_temp = dict[str, tuple[set[str], list[str]]]()
        for slot in slots:
            weekday = calendar.weekday(
                slot.dt_start.year, slot.dt_start.month, slot.dt_start.day
            )  # Получаем номер дня недели в зависимости от даты
            label = WEEKDAYS[weekday][
                2
            ]  # Получаем название дня; [2]-русское название в WEEKDAYS
            sdate = slot.dt_start.strftime(
                "%d.%m.%y"
            )  # Дата (без времени) в формате строки
            time = slot.dt_start.strftime("%H:%M")  # Время (без даты) в формате строки
            if label not in slots_temp:
                slots_temp[label] = (set(), [])
            slots_temp[label][0].add(sdate)
            slots_temp[label][1].append(time)

        for label, slot_info in slots_temp.items():
            response += (
                f"📅: {label}, {slot_info[0].pop()}\n🕐: {', '.join(slot_info[1])}\n\n"
            )
        return response
