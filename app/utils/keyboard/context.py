from uuid import UUID

from attr import dataclass

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


class SendSlotsKeyboardContext(KeyboardContext):
    teacher_uuid: UUID
    operation_type: OperationType


class DaysForStudentsKeyboardContext(KeyboardContext):
    teacher_uuid: UUID
    slots: list[SlotDTO]


class SlotsForStudentsKeyboardContext(KeyboardContext):
    teacher_uuid: UUID
    slots: list[SlotDTO]


class SuccessSlotBindKeyboardContext(KeyboardContext):
    teacher_uuid: UUID
    student_chat_id: int
    username: str
    role: UserRole


class SpecifyWeekKeyboardContext(KeyboardContext):
    callback_data: type[SpecifyWeekMixin]


class LessonOperationKeyboardContext(KeyboardContext):
    lessons: list[LessonDTO]
    callback_cls: type[BaseCallback]


class ConfirmDeletionKeyboardContext(KeyboardContext):
    callback_data_cls: type[BaseDelete]
    callback_data: BaseDelete


class SpecsToUpdateKeyboardContext(KeyboardContext):
    lesson_uuid: UUID
    specs: dict[str, str]
    callback_data_cls: type[BaseUpdate]
