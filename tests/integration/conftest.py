import os
from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy import URL, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from app.database.orm import Lesson, Slot, TeacherStudent, User  # noqa: F401
from app.database.orm.base import Base
from app.repositories.user_repository import UserRepository
from app.schemas.user import CreateUserDTO
from app.utils.enums.bot_values import UserRole

DEFAULT_TEST_DB_NAME = "scheduler_test"
DEFAULT_TEST_DB_USER = "scheduler_test"
DEFAULT_TEST_DB_PASSWORD = "scheduler_test"
DEFAULT_TEST_DB_HOST = "localhost"
DEFAULT_TEST_DB_PORT = 54321


def get_test_database_url() -> URL:
    database_name = os.getenv("TEST_DB_NAME", DEFAULT_TEST_DB_NAME)
    if "test" not in database_name.lower():
        raise RuntimeError(
            "TEST_DB_NAME must contain 'test' to prevent running integration "
            "tests against a non-test database"
        )

    return URL.create(
        drivername="postgresql+asyncpg",
        username=os.getenv("TEST_DB_USER", DEFAULT_TEST_DB_USER),
        password=os.getenv("TEST_DB_PASSWORD", DEFAULT_TEST_DB_PASSWORD),
        host=os.getenv("TEST_DB_HOST", DEFAULT_TEST_DB_HOST),
        port=int(os.getenv("TEST_DB_PORT", str(DEFAULT_TEST_DB_PORT))),
        database=database_name,
    )


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def setup_engine():
    engine = create_async_engine(get_test_database_url())
    try:
        async with engine.connect() as connection:
            await connection.execute(text("select 1"))
    except (OSError, SQLAlchemyError) as exc:
        await engine.dispose()
        pytest.skip(f"PostgreSQL integration database is unavailable: {exc}")

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(loop_scope="session")
async def setup_session(setup_engine):
    async_session_factory = async_sessionmaker(
        setup_engine,
        expire_on_commit=False,
    )
    async with async_session_factory() as session:
        yield session


@pytest_asyncio.fixture(autouse=True, loop_scope="session")
async def clear_tables(setup_engine: AsyncEngine):
    async with setup_engine.begin() as conn:
        await conn.execute(
            text(
                "truncate table teacher_student, slots, lessons, users "
                "restart identity cascade"
            )
        )
    yield


@pytest.fixture
def new_user():
    def wrap(
        *,
        username: str = "test_username",
        role: UserRole = UserRole.STUDENT,
        cnt: int = 1,
    ):
        return CreateUserDTO(
            username=f"{username}_{cnt}",
            firstname=f"firstname_{cnt}",
            lastname=f"lastname_{cnt}",
            role=role,
            chat_id=cnt,
        )

    return wrap


@pytest_asyncio.fixture(loop_scope="session")
async def create_user(setup_session, new_user):
    async def wrap(role: UserRole = UserRole.STUDENT):
        suffix = uuid4().hex
        user = new_user(
            username=f"user_{suffix}",
            role=role,
            cnt=int(suffix[:12], 16),
        )
        return await UserRepository(setup_session).add_user(user)

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
