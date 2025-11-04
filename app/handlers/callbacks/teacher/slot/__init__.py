from .send_slots import router as send_slots_router
from .slots_correct import router as slots_correct_router
from .slots_incorrect import router as slots_incorrect_router
from .add import router as teacher_slot_add_router

slot_routers = [
    send_slots_router,
    slots_correct_router,
    slots_incorrect_router,
    teacher_slot_add_router,
]
