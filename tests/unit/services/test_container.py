from unittest.mock import MagicMock

from app.services.container import Services


def test_services_use_unit_of_work_repositories():
    uow = MagicMock()

    services = Services(uow)

    assert services.user._repository is uow.users
    assert services.teacher._repository is uow.teachers
    assert services.student._repository is uow.students
    assert services.slot._repository is uow.slots
    assert services.lesson._repository is uow.lessons
