from .start import router as start_router
from .my_info import router as info_router
from .new_schedule import router as new_schedule_router
from .make_slots import router as make_slots_router
from .slots_error import router as slots_error_router
from .make_teacher import router as make_teacher_router

command_routers = [
    start_router,
    info_router,
    new_schedule_router,
    make_slots_router,
    slots_error_router,
    make_teacher_router
]