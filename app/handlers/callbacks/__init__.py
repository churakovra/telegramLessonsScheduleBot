from .back_button import router as back_button_router
from .day_button_handle import router as day_button_handle_router
from .main_menu import router as main_menu_router
from .slot_button_handle import router as slot_button_handle_router
from .slots_correct import router as slots_correct_router
from .slots_incorrect import router as slots_incorrect_router
from .teacher_lesson_add import router as teacher_lesson_add_router
from .teacher_slot_add import router as teacher_slot_add_router
from .teacher_student_add import router as teacher_student_add_router
from .user_info import router as user_info_router

callback_routers = [
    back_button_router,
    day_button_handle_router,
    main_menu_router,
    slot_button_handle_router,
    slots_correct_router,
    slots_incorrect_router,
    teacher_lesson_add_router,
    teacher_slot_add_router,
    teacher_student_add_router,
    user_info_router
]
