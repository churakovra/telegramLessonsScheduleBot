import pytest

from app.schemas.user_dto import UserDTO
from app.utils.enums.bot_values import UserRoles
from tests.integration.conftest import Base


@pytest.fixture
def user_data() -> UserDTO:
    return UserDTO.new_dto(
        username="test",
        firstname="test",
        lastname=None,
        role=UserRoles.STUDENT,
        chat_id=12345,
    )


class TestAddUser(Base):

    from app.db.database import url
    async def test_get_user(self, user_data):
        await self.repository.add_user(user_data)
        user = await self.repository.get_user("test")
        assert user
