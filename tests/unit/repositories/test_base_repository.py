from unittest.mock import AsyncMock, MagicMock

import pytest

from app.repositories.base import BaseRepository


@pytest.fixture
def session():
    session = MagicMock()
    session.flush = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.execute = AsyncMock()
    return session


async def test_add_flushes_commits_and_refreshes_by_default(session):
    repository = BaseRepository(session)
    instance = object()

    result = await repository.add(instance)

    assert result is instance
    session.add.assert_called_once_with(instance)
    session.flush.assert_awaited_once_with()
    session.commit.assert_awaited_once_with()
    session.refresh.assert_awaited_once_with(instance)


async def test_add_does_not_commit_inside_unit_of_work(session):
    repository = BaseRepository(session, auto_commit=False)

    await repository.add(object())

    session.flush.assert_awaited_once_with()
    session.commit.assert_not_awaited()


async def test_add_many_ignores_empty_collection(session):
    repository = BaseRepository(session)

    await repository.add_many([])

    session.add_all.assert_not_called()
    session.flush.assert_not_awaited()
    session.commit.assert_not_awaited()


async def test_execute_flushes_without_committing_when_disabled(session):
    repository = BaseRepository(session, auto_commit=False)
    statement = MagicMock()

    await repository.execute(statement)

    session.execute.assert_awaited_once_with(statement)
    session.flush.assert_awaited_once_with()
    session.commit.assert_not_awaited()
