from aiogram.filters.callback_data import CallbackData


class TeacherProfileCallback(CallbackData, prefix="t-profile"):
    edit: bool = False
