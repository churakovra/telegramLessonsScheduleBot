from .add import router as add_router
from .delete import router as delete_router
from .update import router as update_router

lesson_routers = [
    add_router,
    delete_router,
    update_router,
]