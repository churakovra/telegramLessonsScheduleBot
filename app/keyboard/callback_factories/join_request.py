from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class StudentTeacherInfoCallback(CallbackData, prefix="st-teacher-info"):
    teacher_uuid: UUID


class StudentJoinRequestCallback(CallbackData, prefix="st-join-req"):
    teacher_uuid: UUID


class TeacherJoinRequestListCallback(CallbackData, prefix="t-join-list"):
    pass


class TeacherJoinRequestDecisionCallback(CallbackData, prefix="t-join-dec"):
    request_uuid: UUID
    approve: bool
