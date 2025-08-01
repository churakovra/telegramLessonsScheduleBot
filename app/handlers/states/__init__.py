from .lesson import lesson_routers
from .teacher_student import teacher_student_routers
from .wait_for_slots import router as wait_for_slots_router

state_routers = [
    wait_for_slots_router,
]

state_routers.extend(lesson_routers)
state_routers.extend(teacher_student_routers)
