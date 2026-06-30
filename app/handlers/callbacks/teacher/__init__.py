from .feedback import router as feedback_router
from .lesson import router as lesson_router
from .notification import router as notification_router
from .recurrence import router as recurrence_router
from .reschedule import router as reschedule_router
from .send_slots import router as send_slots_router
from .slot import router as slot_router
from .slots_confirm import router as slots_confirm_router
from .statistics import router as statistics_router
from .student import router as student_router

teacher_routers = [
    student_router,
    lesson_router,
    notification_router,
    recurrence_router,
    reschedule_router,
    feedback_router,
    statistics_router,
    slot_router,
    send_slots_router,
    slots_confirm_router,
]
