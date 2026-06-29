from types import SimpleNamespace

import pytest
from pytest_mock import MockerFixture

from app.services.user_service import UserService


@pytest.fixture
def message(mocker: MockerFixture):
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
def services(mocker: MockerFixture):
    user = mocker.create_autospec(UserService, instance=True)
    user.register_user.return_value = mocker.sentinel.user_uuid
    return SimpleNamespace(user=user)


@pytest.fixture
def command(mocker: MockerFixture):
    return SimpleNamespace(
        args="alice_teacher"
    )
