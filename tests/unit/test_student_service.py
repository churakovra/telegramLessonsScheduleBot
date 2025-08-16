from datetime import datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.schemas.student_dto import StudentDTO
from app.services.student_service import StudentService
from app.utils.exceptions.user_exceptions import UserNotFoundException


class TestGetStudent:
    @pytest.fixture(autouse=True)
    def service(self, session_mock):
        self.service = StudentService(session_mock)

    async def test_get_student_success(self, valid_student):
        username = "test-student"

        self.service._repository.get_student = AsyncMock(return_value=valid_student)

        student = await self.service.get_student(username)

        assert isinstance(student, StudentDTO)
        assert student.username == valid_student.username
        self.service._repository.get_student.assert_called_once_with(
            valid_student.username
        )

    async def test_get_student_none_raising_user_not_found_exception(self):
        username = "test-student"

        self.service._repository.get_student = AsyncMock(return_value=None)

        with pytest.raises(UserNotFoundException):
            await self.service.get_student(username)


class TestParseStudents:
    async def test_parse_students_success(self):
        mock_repo = AsyncMock()

        async def get_student_side_effect(username):
            if username in ["student1", "student2"]:
                return StudentDTO(
                    uuid=uuid4(),
                    username=username,
                    firstname="firstname",
                    lastname="lastname",
                    is_student=True,
                    is_teacher=False,
                    is_admin=False,
                    chat_id=123456789456,
                    dt_reg=datetime.now(),
                    dt_edit=datetime.now(),
                )
            raise UserNotFoundException(username, "STUDENT")

        mock_repo.get_student.side_effect = get_student_side_effect

        service = StudentService.__new__(StudentService)
        service._repository = mock_repo

        students_raw = "student1 student2"

        students, unknown_students = await service.parse_students(students_raw)

        assert len(students) == 2
        assert {s.username for s in students} == {"student1", "student2"}
        assert unknown_students == []

    async def test_parse_students_with_unknown(self):
        mock_repo = AsyncMock()

        async def get_student_side_effect(username):
            if username == "known_student":
                return StudentDTO(
                    uuid=uuid4(),
                    username=username,
                    firstname="firstname",
                    lastname="lastname",
                    is_student=True,
                    is_teacher=False,
                    is_admin=False,
                    chat_id=123456789456,
                    dt_reg=datetime.now(),
                    dt_edit=datetime.now(),
                )
            raise UserNotFoundException(username, "STUDENT")

        mock_repo.get_student.side_effect = get_student_side_effect

        service = StudentService.__new__(StudentService)
        service._repository = mock_repo

        students_raw = "known_student unknown_student"

        students, unknown_students = await service.parse_students(students_raw)

        assert len(students) == 1
        assert students[0].username == "known_student"
        assert unknown_students == ["unknown_student"]
