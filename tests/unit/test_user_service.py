from uuid import UUID

import pytest
from pydantic import ValidationError

from app.schemas.user_dto import UserDTO
from app.services.user_service import UserService
from app.utils.enums.bot_values import UserRoles
from app.utils.exceptions.user_exceptions import UserChangeRoleException, UserNotFoundException


valid_user = UserDTO.new_dto(
        username="test-username",
        firstname="test-firstname",
        lastname="test-lastname",
        role=UserRoles.STUDENT,
        chat_id=123456789,
    )

valid_admin = valid_user.model_copy()
valid_admin.is_admin = True

invalid_admin = valid_admin.model_copy()
invalid_admin.is_admin = False

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

class TestAddRole(Base):
    async def test_add_role_success(self, func_mock):
        func_mock(service=self.service._repository, mock_method="get_user", return_value=valid_admin)
        edit_role_mock = func_mock(service=self.service._repository, mock_method="edit_role")

        await self.service.add_role(valid_admin.username, valid_user.username, UserRoles.TEACHER)

        edit_role_mock.assert_awaited_once_with(valid_user.uuid, UserRoles.TEACHER, True)



    @pytest.mark.parametrize(
            "side_effect, expectation",
            [
                ([None, valid_user], UserNotFoundException),
                ([valid_admin, None], UserNotFoundException),
                ([invalid_admin, valid_user], UserChangeRoleException),
            ]
    )
    async def test_add_role_exceptions(self, side_effect, expectation, func_mock):
        func_mock(service=self.service._repository, mock_method="get_user", side_effect=side_effect)

        with pytest.raises(expectation):
            await self.service.add_role(valid_admin.username, valid_user.username, UserRoles.TEACHER)


class TestGetUser(Base):
    async def test_get_user_success(self, func_mock):
        username = "test-username"
        get_user_mock = func_mock(service=self.service._repository, mock_method="get_user", return_value=valid_user)
        
        user = await self.service.get_user(username)
        
        assert user
        assert user.username == username
        get_user_mock.assert_awaited_once_with(username)

    async def test_get_user_raises_user_not_found_exception(self, func_mock):
        username = "unknown_username"
        get_user_mock = func_mock(service=self.service._repository, mock_method="get_user", return_value=None)
        
        with pytest.raises(UserNotFoundException) as exc:
            await self.service.get_user(username)
            assert get_user_mock.assert_awaited_once_with(username)
            assert exc.value.username == username


class TestGetUserInfo(Base):
    async def test_get_user_info_success(self, func_mock):
        func_mock(service=self.service, mock_method="get_user", return_value=valid_user)
        
        info = await self.service.get_user_info(valid_user.username)
        
        assert info
        fields_to_check = ["username", "firstname", "lastname"]
        assert all(str(getattr(valid_user, f)) in info for f in fields_to_check)
