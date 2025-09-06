from unittest.mock import AsyncMock
from uuid import uuid4

from pydantic import ValidationError
import pytest

from app.services.lesson_service import LessonService


class TestCreateLesson:
    @pytest.fixture(autouse=True)
    def service(self, session_mock):
        self.service = LessonService(session_mock)

    @pytest.mark.parametrize(
        "label, duration, uuid_teacher, price, expecting",
        [
            ("test-lesson1", 60, uuid4(), 1000, None),
            ("test-lesson2", 90, uuid4(), 1500, None),
            (None, 60, uuid4(), 1500, ValidationError),
            ("test-lesson-error", 60.5, uuid4(), 1500, ValidationError),
            ("test-lesson-error", None, uuid4(), 1500, ValidationError),
            ("test-lesson-error", 60, None, 1500, ValidationError),
            ("test-lesson-error", 60, uuid4(), 1500.5, ValidationError),
            ("test-lesson-error", 60, uuid4(), None, ValidationError),
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

        if expecting is None:
            new_lesson = await self.service.create_lesson(**lesson)
            assert new_lesson is not None
            self.service._repository.create_lesson.assert_called_once()
        else:
            with pytest.raises(expecting):
                await self.service.create_lesson(**lesson)
