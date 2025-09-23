import pytest
import pytest_asyncio

from app.repositories.teacher_repository import TeacherRepository
from app.utils.enums.bot_values import UserRoles

pytestmark = pytest.mark.asyncio(loop_scope="session")


@pytest_asyncio.fixture(loop_scope="session")
async def prepare_user(insert_user):
    return await insert_user()


class Base:
    @pytest.fixture(autouse=True)
    def setup_repo(self, setup_session):
        self.repo = TeacherRepository(setup_session)


class TestAddTeacher(Base):
    async def test_add_teacher_success(self, prepare_user):
        user = prepare_user[0]
        await self.repo.add_teacher(user.uuid)

        teacher = await self.repo.get_teacher(user.uuid)

        assert teacher.is_teacher
        assert not teacher.is_student


# class TestGetTeacher(Base):
#     async def test_get_teacher_success(self, insert_user):
#         users = await insert_user(role=UserRoles.TEACHER)
#         user = users[0]

#         teacher = await self.repo.get_teacher(user.uuid)

#         assert teacher


# class TestRemoveTeacher(Base):
#     async def test_remove_teacher_success(self, insert_user):
#         users = await insert_user(role=UserRoles.TEACHER)
#         teacher = users[0]

#         removed_teacher = await self.repo.remove_teacher(teacher.uuid)

#         user = self.repo.get_teacher(removed_teacher)

#         assert removed_teacher.uuid == teacher.uuid
#         assert user is None
