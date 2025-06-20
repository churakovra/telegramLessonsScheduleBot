from dataclasses import dataclass
from enum import Enum


class BotValues(str, Enum):
    pass

class UserRoles(BotValues):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    NOT_DEFINED = "not defined"
