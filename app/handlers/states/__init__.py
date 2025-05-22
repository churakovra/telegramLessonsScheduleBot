from .wait_for_teacher_username import router as wait_for_teacher_username_router
from .wait_for_slots import router as wait_for_slots_router

state_routers = [
    wait_for_teacher_username_router,
    wait_for_slots_router
]