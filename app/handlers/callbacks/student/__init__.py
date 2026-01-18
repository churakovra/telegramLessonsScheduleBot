from .days_for_students import router as days_for_students_router
from .slots_for_students import router as slots_for_students_router

student_routers = [days_for_students_router, slots_for_students_router]
