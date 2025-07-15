from .make_teacher import router as make_teacher_router
from .menu import router as menu_router
from .new_slots import router as new_schedule_router
from .start import router as start_router

command_routers = [
    make_teacher_router,
    menu_router,
    new_schedule_router,
    start_router,
]