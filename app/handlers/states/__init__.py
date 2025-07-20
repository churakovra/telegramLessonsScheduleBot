from .lesson import lesson_routers
from .new_slots_ready import router as new_slots_ready_router
from .wait_for_slots import router as wait_for_slots_router
from .wait_for_teacher_students import router as wait_for_teacher_students_router

state_routers = [
    new_slots_ready_router,
    wait_for_slots_router,
    wait_for_teacher_students_router,
]

state_routers.extend(lesson_routers)
