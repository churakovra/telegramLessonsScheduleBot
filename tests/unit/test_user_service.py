import datetime

import pytest

from app.services.user_service import UserService
from app.utils.enums.bot_values import UserRoles


class Base:
    @pytest.fixture(autouse=True)
    def service(self, session_mock):
        self.service = UserService(session_mock)
        return self.service


class TestRegisterUser(Base):
    async def register_user_success(self, func_mock):
        user_data = {
            "username": "test-username",
            "firstname": "test-firstname",
            "role": UserRoles.STUDENT,
            "chat_id": 123456789,
        }

        mock = func_mock(service=self.service._repository, mock_method="add_user")

        new_user = self.service.register_user(**user_data)
        assert new_user.uuid
        assert new_user.dt_reg.date() == datetime.now().date()
        mock.assert_awaited_once()
