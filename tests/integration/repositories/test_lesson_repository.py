import pytest

from app.repositories.lesson_repository import LessonRepository
from app.repositories.teacher_repository import TeacherRepository
from app.schemas.lesson import CreateLessonDTO
from app.utils.enums.bot_values import UserRole

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def test_create_update_and_delete_lesson(setup_session, create_user):
    teacher = await create_user(UserRole.TEACHER)
    repository = LessonRepository(setup_session)
    lesson = await repository.create_lesson(
        CreateLessonDTO(
            label="Algebra",
            duration=60,
            uuid_teacher=teacher.uuid,
            price=1000,
        )
    )

    await repository.update_lesson(lesson.uuid, {"label": "Advanced algebra"})
    updated = await repository.get_lesson_or_none(lesson.uuid)
    assert updated.label == "Advanced algebra"

    await repository.delete_lesson(lesson.uuid)
    assert await repository.get_lesson_or_none(lesson.uuid) is None


async def test_teacher_lessons_are_ordered_and_scoped(setup_session, create_user):
    teacher = await create_user(UserRole.TEACHER)
    other_teacher = await create_user(UserRole.TEACHER)
    repository = LessonRepository(setup_session)
    for label in ("Geometry", "Algebra"):
        await repository.create_lesson(
            CreateLessonDTO(
                label=label,
                duration=60,
                uuid_teacher=teacher.uuid,
                price=1000,
            )
        )
    await repository.create_lesson(
        CreateLessonDTO(
            label="Biology",
            duration=60,
            uuid_teacher=other_teacher.uuid,
            price=1000,
        )
    )

    lessons = await repository.get_teacher_lessons(teacher.uuid)

    assert [lesson.label for lesson in lessons] == ["Algebra", "Geometry"]


async def test_attach_and_detach_student_lesson(setup_session, create_user):
    teacher = await create_user(UserRole.TEACHER)
    student = await create_user(UserRole.STUDENT)
    teachers = TeacherRepository(setup_session)
    lessons = LessonRepository(setup_session)
    lesson = await lessons.create_lesson(
        CreateLessonDTO(
            label="Physics",
            duration=90,
            uuid_teacher=teacher.uuid,
            price=1500,
        )
    )
    await teachers.attach_student(teacher.uuid, student.uuid, None)

    await lessons.attach_lesson(student.uuid, teacher.uuid, lesson.uuid)
    attached = await lessons.get_student_lessons(student.uuid)
    assert [item.uuid for item in attached] == [lesson.uuid]

    await lessons.detach_specific_lesson(student.uuid, teacher.uuid, lesson.uuid)
    assert await lessons.get_student_lessons(student.uuid) == []
