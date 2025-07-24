from .make_teacher import router as make_teacher_router
from .menu import router as menu_router
from .start import router as start_router

command_routers = [
    make_teacher_router,
    menu_router,
    start_router,
]