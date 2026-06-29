from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class FeedbackCallback(CallbackData, prefix="feedback"):
    slot_uuid: UUID
    rating: int


class FeedbackCommentCallback(CallbackData, prefix="feedback-comment"):
    slot_uuid: UUID
    rating: int
    add_comment: bool


class TeacherFeedbackListCallback(CallbackData, prefix="t-feedback-list"):
    pass
