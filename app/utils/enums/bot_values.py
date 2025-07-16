from dataclasses import dataclass
from enum import Enum


class BotEnum(str, Enum):
    pass

class UserRoles(BotEnum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    NOT_DEFINED = "not defined"
