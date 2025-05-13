from .wait_for_slots import router as wait_for_slots_router
from .wait_slots_send import router as wait_slots_send_router

state_routers = [
    wait_for_slots_router,
    wait_slots_send_router
]