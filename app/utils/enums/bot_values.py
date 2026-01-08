from enum import StrEnum


class BotEnum(StrEnum):
    pass


class UserRole(BotEnum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    NOT_DEFINED = "not defined"
    

class OperationType(BotEnum):
    ADD = "add"
    UPDATE = "update"


class WeekFlag(BotEnum):
    CURRENT = "0"
    NEXT = "1"
