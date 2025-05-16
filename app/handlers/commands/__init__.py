from .start import router as start_router
from .new_slots import router as new_schedule_router
from .make_teacher import router as make_teacher_router

command_routers = [
    start_router,
    new_schedule_router,
    make_teacher_router
]