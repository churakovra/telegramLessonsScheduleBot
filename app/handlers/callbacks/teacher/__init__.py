from .lesson import router as lesson_router
from .slot import router as slot_router
from .student import router as student_router

teacher_routers = [
    student_router,
    lesson_router,
    slot_router,
]
