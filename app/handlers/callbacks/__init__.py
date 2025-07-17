from .day_button_handle import router as day_button_handle_router
from .main_menu import router as main_menu_router
from .slot_button_handle import router as slot_button_handle_router
from .slots_correct import router as slots_correct_router
from .slots_incorrect import router as slots_incorrect_router
from .sub_menu import router as sub_menu_router
from .user_info import router as user_info_router

callback_routers = [
    day_button_handle_router,
    main_menu_router,
    slot_button_handle_router,
    slots_correct_router,
    slots_incorrect_router,
    sub_menu_router,
    user_info_router
]
