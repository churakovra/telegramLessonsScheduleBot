from dataclasses import dataclass
from enum import Enum


class BotValues(Enum):
    class UserRoles(Enum):
        ADMIN = "admin"
        TEACHER = "teacher"
        STUDENT = "student"
        NOT_DEFINED = "not defined"
