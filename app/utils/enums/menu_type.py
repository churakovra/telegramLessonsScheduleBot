from enum import StrEnum

class MenuType(StrEnum):
    TEACHER = "t"
    TEACHER_STUDENT = "t-student"
    TEACHER_STUDENT_ADD = "t-student_add"
    TEACHER_STUDENT_UPDATE = "t-student_update"
    TEACHER_STUDENT_LIST = "t-student_list"
    TEACHER_STUDENT_DELETE = "t-student_delete"
    TEACHER_SLOT = "t-slot"
    TEACHER_SLOT_ADD = "t-slot_add"
    TEACHER_SLOT_UPDATE = "t-slot_update"
    TEACHER_SLOT_SPOT = "t-slot_spot"
    TEACHER_SLOT_LIST = "t-slot_list"
    TEACHER_SLOT_DELETE = "t-slot_delete"
    TEACHER_LESSON = "t-lesson"
    TEACHER_LESSON_ADD = "t-lesson_add"
    TEACHER_LESSON_UPDATE = "t-lesson_update"
    TEACHER_LESSON_LIST = "t-lesson_list"
    TEACHER_LESSON_DELETE = "t-lesson_delete"

    STUDENT = "s"
    STUDENT_TEACHER = "s-teacher"
    STUDENT_TEACHER_LIST = "s-teacher_list"
    STUDENT_SLOT = "s-slot"
    STUDENT_SLOT_LIST = "s-slot_list"
    STUDENT_LESSON = "s-lesson"
    STUDENT_LESSON_LIST = "s-lesson_list"

    ADMIN = "a"
    ADMIN_TEMP = "a_temp"
    
    NEW = "n"
