from datetime import UTC, datetime, timedelta

import pytest

from app.repositories.slot_repository import SlotRepository
from app.schemas.slot import CreateSlotDTO
from app.utils.enums.bot_values import UserRole
from app.utils.exceptions.slot_exceptions import SlotAlreadyTakenException

pytestmark = pytest.mark.asyncio(loop_scope="session")


def new_slot(teacher_uuid, *, days=1):
    return CreateSlotDTO(
        uuid_teacher=teacher_uuid,
        dt_start=datetime.now(UTC) + timedelta(days=days),
        uuid_student=None,
        dt_spot=None,
    )


async def test_add_get_assign_and_delete_slot(setup_session, create_user):
    teacher = await create_user(UserRole.TEACHER)
    student = await create_user(UserRole.STUDENT)
    repository = SlotRepository(setup_session)
    slot = new_slot(teacher.uuid)
    await repository.add_slots([slot])

    stored = await repository.get_slot(slot.uuid)
    assert stored.uuid_teacher == teacher.uuid
    assert stored.uuid_student is None

    await repository.assign_slot(student.uuid, slot.uuid)
    assigned = await repository.get_slot(slot.uuid)
    assert assigned.uuid_student == student.uuid
    assert assigned.dt_spot is not None

    await repository.delete_slot(slot.uuid)
    assert await repository.get_slot(slot.uuid) is None


async def test_free_slots_exclude_assigned_and_other_teachers(
    setup_session, create_user
):
    teacher = await create_user(UserRole.TEACHER)
    other_teacher = await create_user(UserRole.TEACHER)
    student = await create_user(UserRole.STUDENT)
    repository = SlotRepository(setup_session)
    free = new_slot(teacher.uuid, days=2)
    assigned = new_slot(teacher.uuid, days=3)
    other = new_slot(other_teacher.uuid, days=2)
    await repository.add_slots([free, assigned, other])
    await repository.assign_slot(student.uuid, assigned.uuid)

    result = await repository.get_free_slots(teacher.uuid)

    assert [slot.uuid for slot in result] == [free.uuid]


async def test_assign_slot_does_not_overwrite_existing_student(
    setup_session, create_user
):
    teacher = await create_user(UserRole.TEACHER)
    first_student = await create_user(UserRole.STUDENT)
    second_student = await create_user(UserRole.STUDENT)
    repository = SlotRepository(setup_session)
    slot = new_slot(teacher.uuid)
    await repository.add_slots([slot])
    await repository.assign_slot(first_student.uuid, slot.uuid)

    with pytest.raises(SlotAlreadyTakenException) as exc:
        await repository.assign_slot(second_student.uuid, slot.uuid)

    assigned = await repository.get_slot(slot.uuid)
    assert exc.value.message == f"Slot {slot.uuid} is already taken"
    assert assigned.uuid_student == first_student.uuid


async def test_delete_slots_ignores_empty_collection(setup_session):
    repository = SlotRepository(setup_session)

    await repository.delete_slots([])
