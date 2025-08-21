import datetime
from uuid import UUID

from pydantic import ValidationError
import pytest

from app.schemas.user_dto import UserDTO
from app.services.user_service import UserService
from app.utils.enums.bot_values import UserRoles


@pytest.fixture
def valid_user():
    return UserDTO.new_dto(
        username="test-username",
        firstname="test-firstname",
        lastname="test-lastname",
        role=UserRoles.STUDENT,
        chat_id=123456789,
    )


class Base:
    @pytest.fixture(autouse=True)
    def service(self, session_mock):
        self.service = UserService(session_mock)
        return self.service


class TestRegisterUser(Base):
    @pytest.mark.parametrize(
        "username, firstname, lastname, role, chat_id, expectation",
        [
            ("test-username", "test-firstname", "test-lastname", UserRoles.STUDENT, 123456789, None),
            ("test-username", "test-firstname", None, UserRoles.STUDENT, 123456789, None),
            (None, "test-firstname", "test-lastname", UserRoles.STUDENT, 123456789, ValidationError),
            ("test-username", None, "test-lastname", UserRoles.STUDENT, 123456789, ValidationError),
            ("test-username", "test-firstname", "test-lastname", UserRoles.STUDENT, None, ValidationError),
        ],
    )
    async def test_register_user_success(self, func_mock, username, firstname, lastname, role, chat_id, expectation):
        mock = func_mock(service=self.service._repository, mock_method="add_user")


        if expectation:
            with pytest.raises(expectation):
                await self.service.register_user(username, firstname, lastname, role, chat_id)
        else:
            new_user_uuid = await self.service.register_user(username, firstname, lastname, role, chat_id)
            assert isinstance(new_user_uuid, UUID)
            mock.assert_awaited_once()
