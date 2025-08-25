from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.schemas.student_dto import StudentDTO
from app.schemas.user_dto import UserDTO


@pytest.fixture
async def session_mock():
    return MagicMock()


@pytest.fixture()
def func_mock(monkeypatch):
    def _mock(
        *, service, mock_method, async_mode=True, side_effect=None, return_value=None
    ):
        mock = AsyncMock if async_mode else MagicMock
        internal_mock = mock(side_effect=side_effect, return_value=return_value)
        monkeypatch.setattr(service, mock_method, internal_mock)
        return internal_mock

    return _mock


@pytest.fixture
def valid_student():
    return StudentDTO(
        uuid=uuid4(),
        username="test-student",
        firstname="firstname",
        lastname="lastname",
        is_student=True,
        is_teacher=False,
        is_admin=False,
        chat_id=123456789456,
        dt_reg=datetime.now(),
        dt_edit=datetime.now(),
    )


@pytest.fixture
def valid_teacher():
    return UserDTO(
        uuid=uuid4(),
        username="test-username",
        firstname="test-firstname",
        lastname="test-lastname",
        is_student=False,
        is_teacher=True,
        is_admin=False,
        chat_id=1234567898765,
        dt_reg=datetime.now(),
        dt_edit=datetime.now(),
    )
