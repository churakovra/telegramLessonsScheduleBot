from unittest.mock import AsyncMock, MagicMock

import pytest

from app.database.unit_of_work import UnitOfWork


@pytest.fixture
def session():
    session = MagicMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    return session


def test_repositories_share_session_and_disable_auto_commit(session):
    uow = UnitOfWork(session)

    repositories = [
        uow.users,
        uow.teachers,
        uow.students,
        uow.slots,
        uow.lessons,
    ]
    assert all(repository.session is session for repository in repositories)
    assert all(repository.auto_commit is False for repository in repositories)


async def test_commit_delegates_to_session(session):
    uow = UnitOfWork(session)

    await uow.commit()

    session.commit.assert_awaited_once_with()


async def test_rollback_delegates_to_session(session):
    uow = UnitOfWork(session)

    await uow.rollback()

    session.rollback.assert_awaited_once_with()
