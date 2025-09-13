import pytest
import pytest_asyncio

from app.db.orm.slot import Slot
from app.db.orm.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_dto import UserDTO

pytestmark = pytest.mark.asyncio(loop_scope="session")


@pytest_asyncio.fixture(loop_scope="session", autouse=True)
async def prepare_student(insert_user):
    student = await insert_user(username="test_username")
    return student[0]


class Base:
    @pytest.fixture(autouse=True)
    def setup_repo(self, setup_session):
        self.repo = UserRepository(setup_session)


class TestAddUser(Base):
    async def test_add_user_success(self, new_user):
        new_user = new_user(username="test_username")
        await self.repo.add_user(new_user)
        user = await self.repo.get_user(new_user.username)

        assert user


class TestGetUser(Base):
    async def test_get_user_success(self, prepare_student):
        user = await self.repo.get_user(prepare_student.username)

        assert user
        assert isinstance(user, UserDTO)

    async def test_get_user_returns_userdto(self, prepare_student):
        user = await self.repo.get_user(prepare_student.username)

        assert isinstance(user, UserDTO)

    async def test_get_user_returns_none(self):
        user = await self.repo.get_user("unknown-username")

        assert not user


