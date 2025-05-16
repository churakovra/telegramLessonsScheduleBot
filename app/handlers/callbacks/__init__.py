from .slots_correct import router as slots_correct_router
from .slots_incorrect import router as slots_incorrect_router
from .user_info import router as user_info_router

callback_routers = [
    slots_correct_router,
    slots_incorrect_router,
    user_info_router
]