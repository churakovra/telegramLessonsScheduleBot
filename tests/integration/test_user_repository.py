import pytest

from app.db.orm.slot import Slot
from app.db.orm.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_dto import UserDTO
from app.utils.enums.bot_values import UserRoles


@pytest.fixture
def user_data() -> UserDTO:
    return UserDTO.new_dto(
        username="test",
        firstname="test",
        lastname=None,
        role=UserRoles.STUDENT,
        chat_id=12345,
    )


class Base:
    @pytest.fixture(autouse=True)
    def setup_repo(self, setup_session):
        self.repo = UserRepository(setup_session)


class TestAddUser(Base):
    async def test_add_user_success(self, user_data):
        await self.repo.add_user(user_data)
        user = await self.repo.get_user("test")
        assert user
