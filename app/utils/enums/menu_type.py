from app.utils.enums.bot_values import BotEnum


class MenuType(BotEnum):
    TEACHER = "cg-t"
    TEACHER_STUDENT = "cg-t-student"
    TEACHER_STUDENT_ADD = "cg-t-student_add"
    TEACHER_STUDENT_update = "cg-t-student_update"
    TEACHER_STUDENT_LIST = "cg-t-student_list"
    TEACHER_STUDENT_DELETE = "cg-t-student_delete"
    TEACHER_SLOT = "cg-t-slot"
    TEACHER_SLOT_ADD = "cg-t-slot_add"
    TEACHER_SLOT_update = "cg-t-slot_update"
    TEACHER_SLOT_SPOT = "cg-t-slot_spot"
    TEACHER_SLOT_LIST = "cg-t-slot_list"
    TEACHER_SLOT_DELETE = "cg-t-slot_delete"
    TEACHER_LESSON = "cg-t-lesson"
    TEACHER_LESSON_ADD = "cg-t-lesson_add"
    TEACHER_LESSON_update = "cg-t-lesson_update"
    TEACHER_LESSON_LIST = "cg-t-lesson_list"
    TEACHER_LESSON_DELETE = "cg-t-lesson_delete"

    STUDENT = "cg-s"
    STUDENT_TEACHER = "cg-s-teacher"
    STUDENT_TEACHER_LIST = "cg-s-teacher_list"
    STUDENT_SLOT = "cg-s-slot"
    STUDENT_SLOT_LIST = "cg-s-slot_list"
    STUDENT_LESSON = "cg-s-lesson"
    STUDENT_LESSON_LIST = "cg-s-lesson_list"

    ADMIN = "cg-a"
    ADMIN_TEMP = "cg-a_temp"
    
    NEW = "cg-n"
