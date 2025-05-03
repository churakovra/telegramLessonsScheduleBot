from .start import router as start_router
from .new_schedule import router as new_schedule_router
from .slots_error import router as slots_error_router
from .new_lesson import router as new_lesson_router

command_routers = [
    start_router,
    new_schedule_router,
    slots_error_router,
    new_lesson_router
]