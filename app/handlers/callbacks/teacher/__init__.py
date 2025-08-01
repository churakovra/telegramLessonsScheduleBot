from .lesson import lesson_routers
from .slot import slot_routers
from .student import student_routers

teacher_routers = []

teacher_routers.extend(lesson_routers)
teacher_routers.extend(slot_routers)
teacher_routers.extend(student_routers)
