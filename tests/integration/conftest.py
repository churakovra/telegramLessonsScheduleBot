import pytest


@pytest.fixture(scope="session", autouse=True)
async def setup_session(): ...