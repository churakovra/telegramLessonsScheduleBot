from dataclasses import dataclass
from uuid import UUID

from app.schemas.lesson_dto import LessonDTO
from app.schemas.slot_dto import SlotDTO
from app.utils.enums.bot_values import OperationType, UserRole
from app.utils.keyboard.callback_factories.common import (
    BaseCallback,
    BaseDelete,
    BaseUpdate,
)
from app.utils.keyboard.callback_factories.mixins import SpecifyWeekMixin


@dataclass
class KeyboardContext:
    pass


@dataclass
class SendSlotsKeyboardContext(KeyboardContext):
    teacher_uuid: UUID
    operation_type: OperationType


@dataclass
class DaysForStudentsKeyboardContext(KeyboardContext):
    teacher_uuid: UUID
    slots: list[SlotDTO]


@dataclass
class SlotsForStudentsKeyboardContext(KeyboardContext):
    teacher_uuid: UUID
    slots: list[SlotDTO]


@dataclass
class SuccessSlotBindKeyboardContext(KeyboardContext):
    teacher_uuid: UUID
    student_chat_id: int
    username: str
    role: UserRole


@dataclass
class SpecifyWeekKeyboardContext(KeyboardContext):
    callback_data: type[SpecifyWeekMixin]


@dataclass
class LessonOperationKeyboardContext(KeyboardContext):
    lessons: list[LessonDTO]
    callback_cls: type[BaseCallback]


@dataclass
class ConfirmDeletionKeyboardContext(KeyboardContext):
    callback_data_cls: type[BaseDelete]
    callback_data: BaseDelete


@dataclass
class SpecsToUpdateKeyboardContext(KeyboardContext):
    lesson_uuid: UUID
    specs: dict[str, str]
    callback_data_cls: type[BaseUpdate]
