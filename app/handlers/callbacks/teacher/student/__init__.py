from .add import router as add_router
from .delete import router as delete_router
from .list import router as list_router

student_routers = [
    add_router,
    delete_router,
    list_router,
]