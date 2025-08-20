from unittest.mock import call
from uuid import uuid4

import pytest

from app.handlers.callbacks import teacher
from app.schemas.user_dto import UserDTO
from app.services.teacher_service import TeacherService, logger
from app.utils.exceptions.teacher_exceptions import TeacherAlreadyHasStudentException
from app.utils.exceptions.user_exceptions import UserNotFoundException


class Base:
    @pytest.fixture(autouse=True)
    def service(self, session_mock):
        self.service = TeacherService(session_mock)
        return self.service


class TestGetTeacher(Base):
    async def test_get_teacher_success(self, valid_teacher, func_mock):
        teacher_username = "test-username"

        func_mock(
            service=self.service._repository,
            mock_method="get_teacher",
            return_value=valid_teacher,
        )

        teacher = await self.service.get_teacher(teacher_username)

        self.service._repository.get_teacher.assert_awaited_once_with(teacher_username)
        assert isinstance(teacher, UserDTO)

    async def test_get_teacher_raising_UserNotFoundException(self, func_mock):
        teacher_username = "unknown-username"

        func_mock(
            service=self.service._repository,
            mock_method="get_teacher",
            return_value=None,
        )

        with pytest.raises(UserNotFoundException) as exc:
            await self.service.get_teacher(teacher_username)

        assert exc.value.data == teacher_username
        assert teacher_username in str(exc.value)


class TestGetTeacherByUUID(Base):
    async def test_get_teacher_by_uuid_success(self, valid_teacher, func_mock):
        teacher_uuid = uuid4()

        func_mock(
            service=self.service._repository,
            mock_method="get_teacher",
            return_value=valid_teacher,
        )

        teacher = await self.service.get_teacher(teacher_uuid)

        self.service._repository.get_teacher.assert_awaited_once_with(teacher_uuid)
        assert isinstance(teacher, UserDTO)

    async def test_get_teacher_by_uuid_raising_user_not_found_exception(
        self, func_mock
    ):
        teacher_uuid = uuid4()

        func_mock(
            service=self.service._repository,
            mock_method="get_teacher",
            return_value=None,
        )

        with pytest.raises(UserNotFoundException) as exc:
            await self.service.get_teacher(teacher_uuid)

        assert exc.value.data == teacher_uuid
        assert str(teacher_uuid) in str(exc.value)


class TestAttachStudents(Base):
    async def test_attach_students_success(self, valid_student, func_mock):
        teacher_uuid = uuid4()
        students_to_attach = [valid_student, valid_student, valid_student]
        uuid_lesson = uuid4()

        func_mock(service=self.service, mock_method="_attach_student")

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
    async def test_attach_student_success(self, valid_student, func_mock):
        teacher_uuid = uuid4()
        uuid_lesson = None

        func_mock(
            service=self.service._repository,
            mock_method="attach_student",
        )

        await self.service._attach_student(
            teacher_uuid, valid_student.uuid, uuid_lesson
        )

        self.service._repository.attach_student.assert_awaited_once_with(
            teacher_uuid, valid_student.uuid, uuid_lesson
        )

    async def test_attach_student_raises_teacher_already_has_student_exception(
        self, func_mock
    ):
        teacher_uuid = uuid4()
        already_attached_student_uuid = uuid4()
        uuid_lesson = None

        func_mock(
            service=self.service._repository,
            mock_method="attach_student",
            side_effect=ValueError,
        )

        logger_mock = func_mock(
            service=logger,
            mock_method="error",
            async_mode=False,
        )

        with pytest.raises(TeacherAlreadyHasStudentException):
            await self.service._attach_student(
                teacher_uuid, already_attached_student_uuid, uuid_lesson
            )

        logger_mock.assert_called_once()


class TestGetStudents(Base):
    async def test_get_students_success(self, valid_student, func_mock):
        teacher_uuid = uuid4()

        mock = func_mock(
            service=self.service._repository,
            mock_method="get_students",
            return_value=[valid_student],
        )

        students = await self.service.get_students(teacher_uuid)

        assert students[0] == valid_student
        mock.assert_awaited_once_with(teacher_uuid)

    async def get_students_raises_teacher_student_not_found(self, func_mock): ...
