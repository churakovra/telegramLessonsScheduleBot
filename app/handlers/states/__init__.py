from .lesson import lesson_routers
from .wait_for_slots import router as wait_for_slots_router
from .wait_for_teacher_students import router as wait_for_teacher_students_router

state_routers = [
    wait_for_slots_router,
    wait_for_teacher_students_router,
]

state_routers.extend(lesson_routers)
