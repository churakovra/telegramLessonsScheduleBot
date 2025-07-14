from .day_button_handle import router as day_button_handle_router
from .menu_teacher_cg import router as menu_teacher_cg_router
from .slot_button_handle import router as slot_button_handle_router
from .slots_correct import router as slots_correct_router
from .slots_incorrect import router as slots_incorrect_router
from .user_info import router as user_info_router

callback_routers = [
    day_button_handle_router,
    menu_teacher_cg_router,
    slot_button_handle_router,
    slots_correct_router,
    slots_incorrect_router,
    user_info_router
]
