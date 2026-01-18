from .lesson import router as lesson_router
from .send_slots import router as send_slots_router
from .slot import router as slot_router
from .slots_confirm import router as slots_confirm_router
from .student import router as student_router

teacher_routers = [
    student_router,
    lesson_router,
    slot_router,
    send_slots_router,
    slots_confirm_router,
]
