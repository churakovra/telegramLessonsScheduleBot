from unittest.mock import MagicMock
import pytest


@pytest.fixture
async def session_mock():
    return MagicMock()