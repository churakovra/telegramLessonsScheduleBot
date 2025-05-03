from .new_lesson_day_callback import router as new_lesson_day_router
from .slots_correct import router as slots_correct_router
from .slots_incorrect import router as slots_incorrect_router

callback_routers = [
    new_lesson_day_router,
    slots_correct_router,
    slots_incorrect_router
]