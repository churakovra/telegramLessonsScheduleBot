from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.schemas.student_dto import StudentDTO
from app.services.student_service import StudentService
from app.utils.exceptions.user_exceptions import UserNotFoundException


@pytest.fixture
def session_mock():
    return MagicMock()


@pytest.fixture
def test_student():
    return StudentDTO(
        uuid=uuid4(),
        username="test-student",
        firstname="firstname",
        lastname="lastname",
        is_student=True,
        is_teacher=False,
        is_admin=False,
        chat_id=123456789456,
        dt_reg=datetime.now(),
        dt_edit=datetime.now(),
    )


class TestGetStudent:
    @pytest.fixture(autouse=True)
    def service(self, session_mock):
        self.service = StudentService(session_mock)

    async def test_get_student_success(self, test_student):
        username = "test-student"

        self.service._repository.get_student = AsyncMock(return_value=test_student)

        student = await self.service.get_student(username)

        assert isinstance(student, StudentDTO)
        assert student.username == test_student.username
        self.service._repository.get_student.assert_called_once_with(
            test_student.username
        )

    async def test_get_student_none_raising_user_not_found_exception(self):
        username = "test-student"

        self.service._repository.get_student = AsyncMock(return_value=None)

        with pytest.raises(UserNotFoundException):
            await self.service.get_student(username)
