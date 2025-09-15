import pytest
import pytest_asyncio

from app.repositories.teacher_repository import TeacherRepository

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
