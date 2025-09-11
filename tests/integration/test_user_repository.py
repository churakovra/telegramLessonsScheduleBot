import pytest
import pytest_asyncio

from app.db.orm.slot import Slot
from app.db.orm.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_dto import UserDTO
from app.utils.enums.bot_values import UserRoles

pytestmark = pytest.mark.asyncio(loop_scope="session")


@pytest.fixture
def user_data() -> UserDTO:
    return UserDTO.new_dto(
        username="test",
        firstname="test",
        lastname=None,
        role=UserRoles.STUDENT,
        chat_id=12345,
    )


@pytest_asyncio.fixture(loop_scope="session")
async def insert_user(
    request,
    setup_session,
):
    params = request.param
    cnt = params.get("cnt", 1)
    role = params.get("role", UserRoles.STUDENT)
    username = params.get("username", None)

    repo = UserRepository(setup_session)

    for i in range(cnt):
        user = UserDTO.new_dto(
            username=username if username else f"username_{i}",
            firstname=f"firstname_{i}",
            lastname=f"lastname_{i}",
            role=role,
            chat_id=i,
        )

        await repo.add_user(user)


class Base:
    @pytest.fixture(autouse=True)
    def setup_repo(self, setup_session):
        self.repo = UserRepository(setup_session)


class TestAddUser(Base):
    async def test_add_user_success(self, user_data):
        await self.repo.add_user(user_data)
        user = await self.repo.get_user("test")
        assert user


class TestGetUser(Base):
    @pytest.mark.parametrize(
        "insert_user", [{"username": "itest-username"}], indirect=True
    )
    async def test_get_user_success(self, insert_user):
        user = await self.repo.get_user("itest-username")

        assert user
        assert isinstance(user, UserDTO)

    async def test_get_user_returns_none(self):
        user = await self.repo.get_user("unknown-username")

        assert not user
