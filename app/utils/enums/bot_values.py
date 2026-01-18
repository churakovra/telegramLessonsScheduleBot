from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    NOT_DEFINED = "not defined"


class ActionType(StrEnum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    LIST = "list"
    INFO = "info"


class WeekFlag(StrEnum):
    CURRENT = "current"
    NEXT = "next"
    UNKNOWN = "unknown"


class EntityType(StrEnum):
    STUDENT = "student"
    SLOT = "slot"
    LESSON = "lesson"
    TEACHER = "teacher"


class KeyboardType(StrEnum):
    TEACHER_MAIN = "main_teacher"
    TEACHER_SUB_STUDENT = "sub_teacher_student"
    TEACHER_SUB_SLOT = "sub_teacher_slot"
    TEACHER_SUB_LESSON = "sub_teacher_lesson"
    STUDENT_MAIN = "main_student"
    STUDENT_SUB_TEACHER = "sub_student_teacher"
    STUDENT_SUB_SLOT = "sub_student_slot"
    ADMIN_MAIN = "main_admin"
    ADMIN_SUB_TEMP = "sub_admin_keyboard"
    IS_SLOTS_CORRECT = "is_slots_correct"
    SEND_SLOTS = "send_slots"
    DAYS_FOR_STUDENTS = "days_for_students"
    SLOTS_FOR_STUDENTS = "slots_for_students"
    SUCCESS_SLOT_BIND = "success_slot_bind"
    SPECIFY_WEEK = "specify_week"
    STUDENT_OPERATION = "student_operation"
    LESSON_OPERATION = "lesson_operation"
    CONFIRM_DELETION = "confirm_deletion"
    SPECS_TO_UPDATE = "specs_to_update"
    ENTITIES_LIST = "entities_list"
    ENTITY_OPERATIONS = "entity_operations"
