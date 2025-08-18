from contextlib import nullcontext as does_not_raise
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.services.lesson_service import LessonService


class TestCreateLesson:
    @pytest.fixture(autouse=True)
    def service(self, session_mock):
        self.service = LessonService(session_mock)

    @pytest.mark.parametrize(
        "label, duration, uuid_teacher, price, expecting",
        [
            ("test-lesson1", 60, uuid4(), 1000, does_not_raise()),
            ("test-lesson2", 90, uuid4(), 1500, does_not_raise()),
        ],
    )
    async def test_create_lesson_success(
        self, label, duration, uuid_teacher, price, expecting
    ):
        self.service._repository.create_lesson = AsyncMock(return_value=uuid4())

        lesson = {
            "label": label,
            "duration": duration,
            "price": price,
            "uuid_teacher": uuid_teacher,
        }

        new_lesson = await self.service.create_lesson(**lesson)

        assert new_lesson is not None
        self.service._repository.create_lesson.assert_called_once()
