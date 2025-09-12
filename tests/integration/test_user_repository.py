import pytest

from app.db.orm.slot import Slot
from app.db.orm.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_dto import UserDTO

pytestmark = pytest.mark.asyncio(loop_scope="session")


class Base:
    @pytest.fixture(autouse=True)
    def setup_repo(self, setup_session):
        self.repo = UserRepository(setup_session)


class TestAddUser(Base):
    async def test_add_user_success(self, new_user):
        await self.repo.add_user(new_user(username="test_username"))
        user = await self.repo.get_user("test_username")

        assert user


@pytest.mark.parametrize("insert_user", [{"username": "test_username"}], indirect=True)
class TestGetUser(Base):
    async def test_get_user_success(self, insert_user):
        user = await self.repo.get_user("test_username")

        assert user
        assert isinstance(user, UserDTO)

    async def test_get_user_returns_userdto(self, insert_user):
        user = await self.repo.get_user("test_username")

        assert isinstance(user, UserDTO)

    async def test_get_user_returns_none(self, insert_user):
        user = await self.repo.get_user("unknown-username")

        assert not user


