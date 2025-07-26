from .lesson import lesson_routers
from .send_slots import router as send_slots_router

from .slots_correct import router as slots_correct_router
from .student import student_routers


from .teacher_slot_add import router as teacher_slot_add_router

teacher_routers = [
    teacher_slot_add_router,
]

teacher_routers.extend(lesson_routers)
teacher_routers.extend(student_routers)
