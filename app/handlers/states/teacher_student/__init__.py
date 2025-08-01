from .wait_for_teacher_students import router as wait_for_teacher_students_router
from .wait_for_student_to_delete import router as wait_for_student_to_delete_router


teacher_student_routers = [
    wait_for_teacher_students_router,
    wait_for_student_to_delete_router,
]