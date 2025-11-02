from enum import Enum


class BotEnum(str, Enum):
    pass


class UserRole(BotEnum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    NOT_DEFINED = "not defined"
