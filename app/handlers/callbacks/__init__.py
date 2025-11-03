from .back_button import router as back_button_router
from .days_for_students import router as day_button_handle_router
from .main_menu import router as main_menu_router
from .slots_for_students import router as slot_button_handle_router
from .user_info import router as user_info_router
from .teacher import teacher_routers
from .common import common_routers

callback_routers = [
    back_button_router,
    day_button_handle_router,
    main_menu_router,
    slot_button_handle_router,
    user_info_router
]

callback_routers.extend(teacher_routers)
callback_routers.extend(common_routers)
