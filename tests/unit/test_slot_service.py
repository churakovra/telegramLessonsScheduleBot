from datetime import datetime
from unittest.mock import MagicMock, AsyncMock
from uuid import uuid4

import pytest

from app.schemas.slot_dto import SlotDTO
from app.services.slot_service import SlotService


@pytest.fixture
def fake_session():
    return MagicMock()


@pytest.fixture
def service(fake_session):
    return SlotService(fake_session)


@pytest.mark.asyncio
async def test_get_slot_success(service):
    slot_uuid = uuid4()
    slot = SlotDTO.new_dto(uuid_teacher=uuid4(), dt_start=datetime.now(), uuid_student=None, dt_spot=None)

    service._repository.get_slot = AsyncMock(return_value=slot)

    result = await service.get_slot(slot_uuid)
    assert result == slot
    service._repository.get_slot.assert_awaited_once_with(slot_uuid)