import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from app.db.database import url
from app.repositories.user_repository import UserRepository
from app.schemas.user_dto import UserDTO
from app.utils.enums.bot_values import UserRole


@pytest.fixture(scope="session")
async def setup_engine():
    engine = create_async_engine(url)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(loop_scope="session")
async def setup_session(setup_engine):
    async_session_factory = async_sessionmaker(setup_engine)
    async with async_session_factory() as session:
        yield session


@pytest_asyncio.fixture(loop_scope="session", autouse=True)
async def clear_tables(setup_engine: AsyncEngine):
    query = "truncate table users restart identity cascade;"
    yield
    async with setup_engine.begin() as conn:
        await conn.execute(text(query))


@pytest.fixture
def new_user():
    def wrap(
        *,
        username: str = "test_username",
        role: UserRole = UserRole.STUDENT,
        cnt: int = 1,
    ):
        return UserDTO.new_dto(
            username=f"{username}_{cnt}",
            firstname=f"firstname_{cnt}",
            lastname=f"lastname_{cnt}",
            role=role,
            chat_id=cnt,
        )

    return wrap


@pytest_asyncio.fixture(loop_scope="session")
async def insert_user(
    setup_session,
    new_user,
):
    async def wrap(
        username: str = "test_username",
        cnt: int = 1,
        role: UserRole = UserRole.STUDENT,
    ):
        inserted_users = []
        repo = UserRepository(setup_session)
        for i in range(cnt):
            user = new_user(username=username, role=role, cnt=i)
            inserted_users.append(user)
            await repo.add_user(user)
        return inserted_users

    return wrap
