import pytest

import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.db.database import url


@pytest.fixture()
async def setup_engine():
    engine = create_async_engine(url)
    yield engine

@pytest_asyncio.fixture(loop_scope="session", scope="session", autouse=True)
async def setup_session(setup_engine):
    async_session_factory = async_sessionmaker(setup_engine) 
    async with async_session_factory()  as session:
        yield session
