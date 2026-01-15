from .common import common_routers
from .common.user_info import router as user_info_router
from .student import student_routers
from .teacher import teacher_routers

callback_routers = [
    user_info_router,
]

callback_routers.extend(common_routers)
callback_routers.extend(teacher_routers)
callback_routers.extend(student_routers)
