from enum import StrEnum


class BotEnum(StrEnum):
    pass


class UserRole(BotEnum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    NOT_DEFINED = "not defined"
