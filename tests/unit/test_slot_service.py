from datetime import datetime
from unittest.mock import MagicMock, AsyncMock
from uuid import uuid4

import pytest

from app.schemas.slot_dto import SlotDTO
from app.services.slot_service import SlotService
from app.utils.exceptions.slot_exceptions import SlotNotFoundException


@pytest.fixture
def session_mock():
    return MagicMock()


class TestGetSlot:
    @pytest.fixture(autouse=True)
    def service(self, session_mock):
        self.service = SlotService(session_mock)

    async def test_get_slot_success(self):
        slot_uuid = uuid4()
        slot = SlotDTO.new_dto(uuid_teacher=uuid4(), dt_start=datetime.now(), uuid_student=None, dt_spot=None)

        self.service._repository.get_slot = AsyncMock(return_value=slot)

        result = await self.service.get_slot(slot_uuid)
        assert result == slot
        self.service._repository.get_slot.assert_awaited_once_with(slot_uuid)

    async def test_get_slot_raising_SlotNotFoundException(self):
        slot_uuid = uuid4()

        self.service._repository.get_slot = AsyncMock(return_value=None)

        with pytest.raises(SlotNotFoundException):
            result = await self.service.get_slot(slot_uuid)
