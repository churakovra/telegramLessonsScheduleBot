from datetime import datetime
from unittest.mock import MagicMock, AsyncMock
from uuid import uuid4

import pytest

from app.schemas.slot_dto import SlotDTO
from app.services.slot_service import SlotService
from app.utils.exceptions.slot_exceptions import (
    SlotNotFoundException,
    SlotFreeNotFoundException,
)


@pytest.fixture
def session_mock():
    return MagicMock()


class TestGetSlot:
    @pytest.fixture(autouse=True)
    def service(self, session_mock):
        self.service = SlotService(session_mock)

    async def test_get_slot_success(self):
        slot_uuid = uuid4()
        slot = SlotDTO.new_dto(
            uuid_teacher=uuid4(),
            dt_start=datetime.now(),
            uuid_student=None,
            dt_spot=None,
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


class TestAddSlot:
    @pytest.fixture(autouse=True)
    def service(self, session_mock):
        self.service = SlotService(session_mock)

    @pytest.fixture
    def valid_slots(self):
        slots: list[SlotDTO] = []
        for _ in range(3):
            slots.append(
                SlotDTO.new_dto(
                    uuid_teacher=uuid4(),
                    dt_start=datetime.now(),
                    uuid_student=None,
                    dt_spot=None,
                )
            )
        return slots

    async def test_all_valid_slots_added(self, valid_slots):
        self.service._repository.add_slot = AsyncMock()

        await self.service.add_slots(valid_slots)

        assert self.service._repository.add_slot.call_count == 3

    async def test_handle_value_error(self, valid_slots):
        self.service._repository.add_slot = AsyncMock(
            side_effect=[None, ValueError, None]
        )

        await self.service.add_slots(valid_slots)

        assert self.service._repository.add_slot.call_count == 3

    async def test_logging_value_error(self, valid_slots, monkeypatch):
        logger_mock = MagicMock()
        monkeypatch.setattr("app.services.slot_service.logger", logger_mock)

        self.service._repository.add_slot = AsyncMock(
            side_effect=[None, ValueError, None]
        )

        await self.service.add_slots(valid_slots)

        assert logger_mock.error.called

    async def test_empty_slots_list_not_use_repository(self):
        empty_slots_list: list[SlotDTO] = []

        self.service._repository.add_slot = AsyncMock()

        await self.service.add_slots(empty_slots_list)

        self.service._repository.add_slot.assert_not_called


class TestGetFreeSlots:
    @pytest.fixture(autouse=True)
    def service(self, session_mock):
        self.service = SlotService(session_mock)

    async def test_get_free_slots_success(self):
        teacher_uuid = uuid4()
        slots = [
            SlotDTO.new_dto(
                uuid_teacher=teacher_uuid,
                dt_start=datetime.now(),
                uuid_student=None,
                dt_spot=None,
            )
        ]

        self.service._repository.get_free_slots = AsyncMock(return_value=slots)

        result = await self.service.get_free_slots(teacher_uuid)
        assert result == slots
        self.service._repository.get_free_slots.assert_awaited_once_with(teacher_uuid)

    async def test_get_free_slots_raises_slot_free_not_found_exception(self):
        teacher_uuid = uuid4()

        self.service._repository.get_free_slots = AsyncMock(return_value=[])

        with pytest.raises(SlotFreeNotFoundException):
            await self.service.get_free_slots(teacher_uuid)
