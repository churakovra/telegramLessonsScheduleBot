from .send_slots import router as send_slots_router

from .slots_correct import router as slots_correct_router

from .teacher_lesson_add import router as teacher_lesson_add_router
from .teacher_slot_add import router as teacher_slot_add_router
from .teacher_student_add import router as teacher_student_add_router
from .teacher_student_delete import router as teacher_student_delete_router
from .teacher_student_list import router as teacher_student_list_router

teacher_routers = [
    teacher_lesson_add_router,
    teacher_slot_add_router,
    teacher_student_add_router,
    teacher_student_delete_router,
    teacher_student_list_router,
]