from .wait_for_lesson_update import router as update_router
from .wait_for_teacher_lesson_duration import router as duration_router
from .wait_for_teacher_lesson_label import router as label_router
from .wait_for_teacher_lesson_price import router as price_router

lesson_routers = [
    update_router,
    duration_router,
    label_router,
    price_router
]