from .days_for_students import router as days_for_students_router
from .feedback import router as feedback_router
from .schedule import router as schedule_router
from .slots_for_students import router as slots_for_students_router
from .statistics import router as statistics_router

student_routers = [
    days_for_students_router,
    slots_for_students_router,
    schedule_router,
    feedback_router,
    statistics_router,
]
