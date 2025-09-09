import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.database import url
from app.repositories.user_repository import UserRepository


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


class Base:
    @pytest.fixture(autouse=True)
    def init_repo(self, setup_session):
        self.repository = UserRepository(setup_session)
