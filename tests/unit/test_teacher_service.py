from unittest.mock import AsyncMock, MagicMock, call
from uuid import uuid4

import pytest

from app.schemas.user_dto import UserDTO
from app.services.teacher_service import TeacherService
from app.utils.exceptions.teacher_exceptions import TeacherAlreadyHasStudentException
from app.utils.exceptions.user_exceptions import UserNotFoundException


@pytest.fixture
def get_teacher_mock():
    def _mock(service, return_value: UserDTO | None):
        service._repository.get_teacher = AsyncMock(return_value=return_value)

    return _mock


class Base:
    @pytest.fixture(autouse=True)
    def service(self, session_mock):
        self.service = TeacherService(session_mock)
        return self.service


class TestGetTeacher(Base):
    async def test_get_teacher_success(self, valid_teacher, get_teacher_mock):
        teacher_username = "test-username"

        get_teacher_mock(self.service, valid_teacher)

        teacher = await self.service.get_teacher(teacher_username)

        self.service._repository.get_teacher.assert_awaited_once_with(teacher_username)
        assert isinstance(teacher, UserDTO)

    async def test_get_teacher_raising_UserNotFoundException(self, get_teacher_mock):
        teacher_username = "unknown-username"

        get_teacher_mock(self.service, None)

        with pytest.raises(UserNotFoundException) as exc:
            await self.service.get_teacher(teacher_username)

        assert exc.value.data == teacher_username
        assert teacher_username in str(exc.value)


class TestGetTeacherByUUID(Base):
    async def test_get_teacher_by_uuid_success(self, valid_teacher, get_teacher_mock):
        teacher_uuid = uuid4()

        get_teacher_mock(self.service, valid_teacher)

        teacher = await self.service.get_teacher(teacher_uuid)

        self.service._repository.get_teacher.assert_awaited_once_with(teacher_uuid)
        assert isinstance(teacher, UserDTO)

    async def test_get_teacher_by_uuid_raising_user_not_found_exception(
        self, get_teacher_mock
    ):
        teacher_uuid = uuid4()

        get_teacher_mock(self.service, None)

        with pytest.raises(UserNotFoundException) as exc:
            await self.service.get_teacher(teacher_uuid)

        assert exc.value.data == teacher_uuid
        assert str(teacher_uuid) in str(exc.value)


class TestAttachStudents(Base):
    async def test_attach_students_success(self, monkeypatch, valid_student):
        teacher_uuid = uuid4()
        students_to_attach = [valid_student, valid_student, valid_student]
        uuid_lesson = uuid4()

        monkeypatch.setattr(self.service, "_attach_student", AsyncMock())

        await self.service.attach_students(
            teacher_uuid=teacher_uuid,
            students=students_to_attach,
            uuid_lesson=uuid_lesson,
        )

        expected_calls = [
            call(teacher_uuid, s.uuid, uuid_lesson) for s in students_to_attach
        ]

        self.service._attach_student.assert_has_calls(expected_calls)
        assert self.service._attach_student.call_count == len(students_to_attach)


class TestAttachStudent(Base):
    @pytest.fixture()
    def repository_mock(self, service):
        def _mock(side_effect):
            service._repository.attach_student = AsyncMock(side_effect=side_effect)

        return _mock

    async def test_attach_student_success(self, valid_student, repository_mock):
        teacher_uuid = uuid4()
        uuid_lesson = None

        repository_mock(side_effect=None)

        await self.service._attach_student(
            teacher_uuid, valid_student.uuid, uuid_lesson
        )

        self.service._repository.attach_student.assert_awaited_once_with(
            teacher_uuid, valid_student.uuid, uuid_lesson
        )

    async def test_attach_student_raises_teacher_already_has_student_exception(
        self, repository_mock, monkeypatch
    ):
        teacher_uuid = uuid4()
        already_attached_student_uuid = uuid4()
        uuid_lesson = None

        repository_mock(side_effect=ValueError)
        logger_mock = MagicMock()
        monkeypatch.setattr("app.services.teacher_service.logger.error", logger_mock)

        with pytest.raises(TeacherAlreadyHasStudentException) as e:
            await self.service._attach_student(
                teacher_uuid, already_attached_student_uuid, uuid_lesson
            )

        logger_mock.assert_called_once()
