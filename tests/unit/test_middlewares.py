from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.middlewares.db_session import DBSessionMiddleware
from app.middlewares.sender_injection import SenderInjectionMiddleware
from app.middlewares.services import ServicesMiddleware
from app.middlewares.user import UserMiddleware
from app.notifier.sender import MessageSender
from app.utils.exceptions.user_exceptions import UserNotFoundException


class SessionContext:
    def __init__(self, session):
        self.session = session

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, exc_type, exc, traceback):
        return None


async def test_db_session_commits_successful_handler():
    session = MagicMock()
    handler = AsyncMock(return_value="result")
    uow = MagicMock()
    uow.commit = AsyncMock()
    uow.rollback = AsyncMock()

    with (
        patch(
            "app.middlewares.db_session.async_session_factory",
            return_value=SessionContext(session),
        ),
        patch("app.middlewares.db_session.UnitOfWork", return_value=uow),
    ):
        data = {}
        result = await DBSessionMiddleware()(handler, MagicMock(), data)

    assert result == "result"
    assert data == {"session": session, "uow": uow}
    uow.commit.assert_awaited_once_with()
    uow.rollback.assert_not_awaited()


async def test_db_session_rolls_back_failed_handler():
    session = MagicMock()
    handler = AsyncMock(side_effect=RuntimeError("handler failed"))
    uow = MagicMock()
    uow.commit = AsyncMock()
    uow.rollback = AsyncMock()

    with (
        patch(
            "app.middlewares.db_session.async_session_factory",
            return_value=SessionContext(session),
        ),
        patch("app.middlewares.db_session.UnitOfWork", return_value=uow),
    ):
        with pytest.raises(RuntimeError, match="handler failed"):
            await DBSessionMiddleware()(handler, MagicMock(), {})

    uow.rollback.assert_awaited_once_with()
    uow.commit.assert_not_awaited()


async def test_services_middleware_injects_container():
    handler = AsyncMock(return_value="ok")
    uow = MagicMock()
    data = {"uow": uow}

    with patch("app.middlewares.services.Services") as services_cls:
        result = await ServicesMiddleware()(handler, MagicMock(), data)

    assert result == "ok"
    services_cls.assert_called_once_with(uow)
    assert data["services"] is services_cls.return_value


async def test_sender_middleware_uses_dispatcher_sender():
    handler = AsyncMock()
    sender = MessageSender(bot=MagicMock())
    data = {"dispatcher": SimpleNamespace(sender=sender)}

    await SenderInjectionMiddleware()(handler, MagicMock(), data)

    assert data["sender"] is sender


async def test_sender_middleware_falls_back_to_context_bot():
    handler = AsyncMock()
    bot = MagicMock()
    data = {"dispatcher": SimpleNamespace(sender=None), "bot": bot}

    await SenderInjectionMiddleware()(handler, MagicMock(), data)

    assert data["sender"].bot is bot


async def test_user_middleware_injects_found_user():
    user = MagicMock()
    services = MagicMock()
    services.user.get_user = AsyncMock(return_value=user)
    handler = AsyncMock()
    event = SimpleNamespace(
        message=SimpleNamespace(from_user=SimpleNamespace(username="alice")),
        callback_query=None,
    )
    data = {"services": services}

    await UserMiddleware()(handler, event, data)

    assert data["user"] is user
    services.user.get_user.assert_awaited_once_with("alice")


async def test_user_middleware_continues_when_user_is_unknown():
    services = MagicMock()
    services.user.get_user = AsyncMock(
        side_effect=UserNotFoundException("alice", "user")
    )
    handler = AsyncMock()
    event = SimpleNamespace(
        message=SimpleNamespace(from_user=SimpleNamespace(username="alice")),
        callback_query=None,
    )
    data = {"services": services}

    await UserMiddleware()(handler, event, data)

    assert "user" not in data
    handler.assert_awaited_once()
