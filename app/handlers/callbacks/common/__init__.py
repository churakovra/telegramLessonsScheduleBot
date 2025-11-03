from .back_button import router as back_button_router
from .main_menu import router as main_menu_router
from .new_menu import router as new_menu_router
from .resend_slots import router as resend_slots_router

common_routers = [
    back_button_router,
    main_menu_router,
    new_menu_router,
    resend_slots_router,
]
