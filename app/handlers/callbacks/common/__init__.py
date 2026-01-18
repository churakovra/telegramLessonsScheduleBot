from .menu_navigation import router as main_menu_router
from .new_menu import router as new_menu_router
from .resend_slots import router as resend_slots_router

common_routers = [
    main_menu_router,
    new_menu_router,
    resend_slots_router,
]
