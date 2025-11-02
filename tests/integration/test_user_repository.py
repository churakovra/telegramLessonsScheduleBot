import pytest
import pytest_asyncio

from app.db.orm.slot import Slot
from app.db.orm.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_dto import UserDTO
from app.utils.enums.bot_values import UserRole

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


class TestEditRole(Base):
    @pytest.mark.parametrize(
        "is_admin, is_student, is_teacher",
        [
            (False, False, False),
            (True, False, False),
            (False, True, False),
            (False, False, True),
            (True, True, False),
            (True, False, True),
            (False, True, True),
            (True, True, True),
        ],
    )
    async def test_edit_role_success(
        self,
        prepare_student,
        is_admin,
        is_student,
        is_teacher,
    ):
        await self.repo.edit_role(prepare_student.uuid, UserRole.ADMIN, is_admin)
        await self.repo.edit_role(prepare_student.uuid, UserRole.STUDENT, is_student)
        await self.repo.edit_role(prepare_student.uuid, UserRole.TEACHER, is_teacher)

        user = await self.repo.get_user(prepare_student.username)

        assert user.is_admin == is_admin
        assert user.is_student == is_student
        assert user.is_teacher == is_teacher

    async def test_edit_role_raises_value_error_with_unknown_role(
        self,
        prepare_student,
        func_mock,
    ):
        with pytest.raises(ValueError):
            await self.repo.edit_role(prepare_student.uuid, UserRole.NOT_DEFINED, True)
