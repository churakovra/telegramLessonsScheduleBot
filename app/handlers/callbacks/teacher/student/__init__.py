from .teacher_student_add import router as teacher_student_add_router
from .teacher_student_delete import router as teacher_student_delete_router
from .teacher_student_list import router as teacher_student_list_router

student_routers = [
    teacher_student_add_router,
    teacher_student_delete_router,
    teacher_student_list_router,
]