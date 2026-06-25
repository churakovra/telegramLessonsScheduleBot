from types import SimpleNamespace

import pytest

from app.services.user_service import UserService


@pytest.fixture
def message(mocker):
    return SimpleNamespace(
        from_user=SimpleNamespace(
            id=42,
            username="alice",
            first_name="Alice",
            last_name="Smith",
        ),
        answer=mocker.AsyncMock(),
    )


@pytest.fixture
def services(mocker):
    user = mocker.create_autospec(UserService, instance=True)
    user.register_user.return_value = mocker.sentinel.user_uuid
    return SimpleNamespace(user=user)
