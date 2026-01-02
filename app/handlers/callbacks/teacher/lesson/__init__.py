from .add import router as add_router
from .delete import router as delete_router

lesson_routers = [
    add_router,
    delete_router,
]