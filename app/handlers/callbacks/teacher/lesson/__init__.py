from .teacher_lesson_add import router as teacher_lesson_add_router
from .teacher_lesson_delete import router as teacher_lesson_delete_router

lesson_routers = [
    teacher_lesson_add_router,
    teacher_lesson_delete_router,
]