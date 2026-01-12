from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    NOT_DEFINED = "not defined"
    

class OperationType(StrEnum):
    ADD = "add"
    UPDATE = "update"


class WeekFlag(StrEnum):
    CURRENT = "0"
    NEXT = "1"


class KeyboardType(StrEnum):
    TEACHER_MAIN = "main_teacher_keyboard"
    TEACHER_SUB = "sub_teacher_keyboard"
    STUDENT_MAIN = "main_student_keyboard"
    STUDENT_SUB = "sub_student_keyboard"