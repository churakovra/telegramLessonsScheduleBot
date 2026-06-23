import pytest

from app.repositories.student_repository import StudentRepository
from app.repositories.teacher_repository import TeacherRepository
from app.utils.enums.bot_values import UserRole

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def test_get_student_by_username_and_uuid(setup_session, create_user):
    student = await create_user(UserRole.STUDENT)
    repository = StudentRepository(setup_session)

    by_username = await repository.get_student_by_username(student.username)
    by_uuid = await repository.get_student_by_uuid(student.uuid)

    assert by_username == student
    assert by_uuid == student


async def test_teacher_students_are_scoped_to_teacher(setup_session, create_user):
    teacher = await create_user(UserRole.TEACHER)
    other_teacher = await create_user(UserRole.TEACHER)
    student = await create_user(UserRole.STUDENT)
    other_student = await create_user(UserRole.STUDENT)
    teachers = TeacherRepository(setup_session)
    await teachers.attach_student(teacher.uuid, student.uuid, None)
    await teachers.attach_student(other_teacher.uuid, other_student.uuid, None)

    students = await StudentRepository(setup_session).get_students_by_teacher_uuid(
        teacher.uuid
    )

    assert [item.uuid for item in students] == [student.uuid]


async def test_non_student_is_not_returned(setup_session, create_user):
    teacher = await create_user(UserRole.TEACHER)

    result = await StudentRepository(setup_session).get_student_by_username(
        teacher.username
    )

    assert result is None
