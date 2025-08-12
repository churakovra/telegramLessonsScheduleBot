from http import server
import select
from unittest.mock import AsyncMock, MagicMock
import pytest

from app.services.student_service import StudentService
from app.utils.exceptions.user_exceptions import UserNotFoundException


@pytest.fixture
def session_mock():
    return MagicMock()

class TestGetStudent:
    @pytest.fixture(autouse=True)
    def service(self, session_mock):
        self.service = StudentService(session_mock)

    async def test_get_student_none_raising_user_not_found_exception(self):
        username = 'test-student'

        self.service._repository.get_student = AsyncMock(return_value=None)

        with pytest.raises(UserNotFoundException):
            await self.service.get_student(username)