from .add import router as add_router
from .list import router as list_router
from .send_slots import router as send_slots_router
from .slots_correct import router as slots_correct_router
from .slots_incorrect import router as slots_incorrect_router
from .update import router as update_router

slot_routers = [
    add_router,
    list_router,
    send_slots_router,
    slots_correct_router,
    slots_incorrect_router,
    update_router,
]
