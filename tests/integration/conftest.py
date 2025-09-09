import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from app.db.database import url


@pytest.fixture(scope="session")
async def setup_engine():
    engine = create_async_engine(url)
    yield engine
    await engine.dispose()


@pytest.fixture
async def setup_session(setup_engine):
    async_session_factory = async_sessionmaker(setup_engine)
    async with async_session_factory() as session:
        yield session


@pytest.fixture(autouse=True)
async def clear_tables(setup_engine: AsyncEngine):
    query = "truncate table users restart identity cascade;"
    yield
    async with setup_engine.begin() as conn:
        await conn.execute(text(query))
