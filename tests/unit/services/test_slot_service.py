from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.schemas.slot import CreateSlotDTO, SlotDTO
from app.services.slot_service import SlotService
from app.utils.enums.bot_values import WeekFlag
from app.utils.exceptions.slot_exceptions import (
    SlotConflictException,
    SlotFreeNotFoundException,
    SlotNotFoundException,
)


@pytest.fixture
def slots_single_element():
    return [
        SlotDTO(
            id=1,
            uuid=uuid4(),
            uuid_teacher=uuid4(),
            dt_start=datetime.now(),
            dt_add=datetime.now(),
            uuid_student=None,
            dt_spot=None,
            created_at=datetime.now(),
            last_updated_at=datetime.now(),
        )
    ]


@pytest.fixture
def slots_multiple_elements():
    slots = []
    for idx in range(3):
        slots.append(
            SlotDTO(
                id=idx,
                uuid=uuid4(),
                uuid_teacher=uuid4(),
                dt_start=datetime.now(),
                dt_add=datetime.now(),
                uuid_student=None,
                dt_spot=None,
                created_at=datetime.now(),
                last_updated_at=datetime.now(),
            )
        )
    return slots


class TestAddSlot:
    @pytest.fixture(autouse=True)
    def service(self, session_mock):
        self.service = SlotService(session_mock)

    async def test_all_valid_slots_added(self, slots_multiple_elements):
        self.service._repository.add_slots = AsyncMock()
        self.service._repository.find_slots_by_starts = AsyncMock(return_value=[])

        await self.service.add_slots(slots_multiple_elements)

        self.service._repository.add_slots.assert_awaited_once_with(
            slots_multiple_elements
        )

    async def test_handle_value_error(self, slots_multiple_elements):
        self.service._repository.add_slots = AsyncMock(side_effect=ValueError)
        self.service._repository.find_slots_by_starts = AsyncMock(return_value=[])

        with pytest.raises(ValueError):
            await self.service.add_slots(slots_multiple_elements)

    async def test_empty_slots_list_not_use_repository(self):
        empty_slots_list = []

        self.service._repository.add_slots = AsyncMock()

        await self.service.add_slots(empty_slots_list)

        self.service._repository.add_slots.assert_not_called()

    async def test_existing_slot_start_raises_conflict(self, slots_multiple_elements):
        self.service._repository.add_slots = AsyncMock()
        self.service._repository.find_slots_by_starts = AsyncMock(
            return_value=[slots_multiple_elements[0]]
        )

        with pytest.raises(SlotConflictException):
            await self.service.add_slots(slots_multiple_elements)

        self.service._repository.add_slots.assert_not_called()


class TestUpdateSlots:
    @pytest.fixture(autouse=True)
    def service(self, session_mock):
        self.service = SlotService(session_mock)

    @staticmethod
    def _slot(*, teacher_uuid, dt_start, student_uuid=None):
        return SlotDTO(
            id=1,
            uuid=uuid4(),
            uuid_teacher=teacher_uuid,
            dt_start=dt_start,
            dt_add=datetime(2026, 7, 1, 10, 0),
            uuid_student=student_uuid,
            dt_spot=datetime(2026, 7, 1, 11, 0) if student_uuid else None,
            created_at=datetime(2026, 7, 1, 10, 0),
            last_updated_at=datetime(2026, 7, 1, 10, 0),
        )

    @staticmethod
    def _new_slot(*, teacher_uuid, dt_start):
        return CreateSlotDTO(
            uuid_teacher=teacher_uuid,
            dt_start=dt_start,
            uuid_student=None,
            dt_spot=None,
        )

    async def test_update_slots_diffs_only_free_slots_and_keeps_booked_slots(self):
        teacher_uuid = uuid4()
        student_uuid = uuid4()
        old_free_removed = self._slot(
            teacher_uuid=teacher_uuid,
            dt_start=datetime(2026, 7, 6, 10, 0),
        )
        old_booked_kept = self._slot(
            teacher_uuid=teacher_uuid,
            dt_start=datetime(2026, 7, 6, 11, 0),
            student_uuid=student_uuid,
        )
        old_free_kept = self._slot(
            teacher_uuid=teacher_uuid,
            dt_start=datetime(2026, 7, 6, 12, 0),
        )
        new_slot = self._new_slot(
            teacher_uuid=teacher_uuid,
            dt_start=datetime(2026, 7, 6, 13, 0),
        )
        slots = [
            self._new_slot(
                teacher_uuid=teacher_uuid,
                dt_start=old_booked_kept.dt_start,
            ),
            self._new_slot(
                teacher_uuid=teacher_uuid,
                dt_start=old_free_kept.dt_start,
            ),
            new_slot,
        ]
        self.service._repository.get_slots = AsyncMock(
            return_value=[old_free_removed, old_booked_kept, old_free_kept]
        )
        self.service._repository.find_slots_by_starts = AsyncMock(return_value=[])
        self.service._repository.delete_slots = AsyncMock()
        self.service._repository.add_slots = AsyncMock()

        await self.service.update_slots(slots, teacher_uuid)

        self.service._repository.delete_slots.assert_awaited_once_with(
            slots=[old_free_removed]
        )
        self.service._repository.add_slots.assert_awaited_once_with(
            slots_dto=[new_slot]
        )

    async def test_update_slots_skips_existing_free_slot_with_same_local_time(self):
        teacher_uuid = uuid4()
        utc3 = timezone(timedelta(hours=3))
        existing_free = self._slot(
            teacher_uuid=teacher_uuid,
            dt_start=datetime(2026, 7, 6, 10, 0, tzinfo=utc3),
        )
        slots = [
            self._new_slot(
                teacher_uuid=teacher_uuid,
                dt_start=datetime(2026, 7, 6, 10, 0),
            )
        ]
        self.service._repository.get_slots = AsyncMock(return_value=[existing_free])
        self.service._repository.find_slots_by_starts = AsyncMock(
            return_value=[existing_free]
        )
        self.service._repository.delete_slots = AsyncMock()
        self.service._repository.add_slots = AsyncMock()

        await self.service.update_slots(slots, teacher_uuid)

        self.service._repository.find_slots_by_starts.assert_not_awaited()
        self.service._repository.delete_slots.assert_awaited_once_with(slots=[])
        self.service._repository.add_slots.assert_awaited_once_with(slots_dto=[])


class TestDeleteFreeSlots:
    @pytest.fixture(autouse=True)
    def service(self, session_mock):
        self.service = SlotService(session_mock)

    @staticmethod
    def _slot(*, teacher_uuid, dt_start, student_uuid=None):
        return SlotDTO(
            id=1,
            uuid=uuid4(),
            uuid_teacher=teacher_uuid,
            dt_start=dt_start,
            dt_add=datetime(2026, 7, 1, 10, 0),
            uuid_student=student_uuid,
            dt_spot=datetime(2026, 7, 1, 11, 0) if student_uuid else None,
            created_at=datetime(2026, 7, 1, 10, 0),
            last_updated_at=datetime(2026, 7, 1, 10, 0),
        )

    async def test_delete_free_slots_keeps_booked_slots(self):
        teacher_uuid = uuid4()
        free_slot = self._slot(
            teacher_uuid=teacher_uuid,
            dt_start=datetime(2026, 7, 6, 10, 0),
        )
        booked_slot = self._slot(
            teacher_uuid=teacher_uuid,
            dt_start=datetime(2026, 7, 6, 11, 0),
            student_uuid=uuid4(),
        )
        self.service._repository.get_slots = AsyncMock(
            return_value=[free_slot, booked_slot]
        )
        self.service._repository.delete_slots = AsyncMock()

        deleted_count = await self.service.delete_free_slots(
            teacher_uuid,
            WeekFlag.CURRENT,
        )

        assert deleted_count == 1
        self.service._repository.delete_slots.assert_awaited_once_with(
            slots=[free_slot]
        )


class TestGetSlot:
    @pytest.fixture(autouse=True)
    def service(self, session_mock):
        self.service = SlotService(session_mock)

    async def test_get_slot_success(self):
        slot_uuid = uuid4()
        slot = SlotDTO(
            id=1,
            uuid=uuid4(),
            uuid_teacher=uuid4(),
            dt_start=datetime.now(),
            dt_add=datetime.now(),
            uuid_student=None,
            dt_spot=None,
            created_at=datetime.now(),
            last_updated_at=datetime.now(),
        )

        self.service._repository.get_slot = AsyncMock(return_value=slot)

        result = await self.service.get_slot(slot_uuid)
        assert result == slot
        self.service._repository.get_slot.assert_awaited_once_with(slot_uuid)

    async def test_get_slot_raises_slot_not_found_exception(self):
        slot_uuid = uuid4()

        self.service._repository.get_slot = AsyncMock(return_value=None)

        with pytest.raises(SlotNotFoundException):
            await self.service.get_slot(slot_uuid)


class TestParseSlots:
    async def test_parse_slots_keeps_teacher_wall_clock_time_in_moscow_timezone(self):
        teacher_uuid = uuid4()

        slots = await SlotService.parse_slots(
            message_text="Tuesday 12:20",
            uuid_teacher=teacher_uuid,
            week_flag=WeekFlag.CURRENT,
        )

        assert len(slots) == 1
        assert slots[0].dt_start.hour == 12
        assert slots[0].dt_start.minute == 20
        assert slots[0].dt_start.utcoffset() == timedelta(hours=3)


class TestGetFreeSlots:
    @pytest.fixture(autouse=True)
    def service(self, session_mock):
        self.service = SlotService(session_mock)

    async def test_get_free_slots_success(self, slots_single_element):
        teacher_uuid = uuid4()

        self.service._repository.get_free_slots = AsyncMock(
            return_value=slots_single_element
        )

        result = await self.service.get_free_slots(teacher_uuid)
        assert result == slots_single_element
        self.service._repository.get_free_slots.assert_awaited_once_with(teacher_uuid)

    async def test_get_free_slots_raises_slot_free_not_found_exception(self):
        teacher_uuid = uuid4()

        self.service._repository.get_free_slots = AsyncMock(return_value=[])

        with pytest.raises(SlotFreeNotFoundException):
            await self.service.get_free_slots(teacher_uuid)


class TestGetDaySlots:
    @pytest.fixture(autouse=True)
    def service(self, session_mock):
        self.service = SlotService(session_mock)

    @pytest.fixture(autouse=True)
    def slot_params(self):
        self.dt = datetime.now()
        self.teacher_uuid = uuid4()

    async def test_get_day_slots_success(self, slots_single_element):
        self.service._repository.get_day_free_slots = AsyncMock(
            return_value=slots_single_element
        )

        slots = await self.service.get_day_slots(self.dt, self.teacher_uuid)

        assert slots == slots_single_element
        self.service._repository.get_day_free_slots.assert_awaited_once_with(
            self.dt, self.teacher_uuid
        )

    async def test_get_day_slots_empty_raises_slot_free_not_found_exception(self):
        self.service._repository.get_day_free_slots = AsyncMock(return_value=[])

        with pytest.raises(SlotFreeNotFoundException):
            await self.service.get_day_slots(self.dt, self.teacher_uuid)
