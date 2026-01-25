from enum import StrEnum

class MenuType(StrEnum):
    TEACHER = "T"
    TEACHER_STUDENT = "T-S"
    TEACHER_SLOT = "T-SL"
    TEACHER_LESSON = "T-L"
    STUDENT = "S"
    STUDENT_TEACHER = "S-T"
    STUDENT_SLOT = "S-SL"
    STUDENT_LESSON = "S-L"
    ADMIN = "A"
    ADMIN_TEMP = "A-TEMP"
    NEW = "NEW"
    CONFIRMATION = "CNFRM"
    CANCEL = "C"
