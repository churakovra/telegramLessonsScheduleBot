from aiogram.types import InlineKeyboardMarkup

from app.schemas.bot_message import BotMessage
from app.utils.bot_strings import BotStrings


def main_menu_message(username: str, markup: InlineKeyboardMarkup) -> BotMessage:
    return BotMessage(
        text=BotStrings.Common.MENU.format(user=username),
        reply_markup=markup,
    )


def slots_added_for_student_message(
    parsed_slots_reply: str, markup: InlineKeyboardMarkup
):
    return BotMessage(
        text=f"{BotStrings.Student.SLOTS_ADDED}\n\n{parsed_slots_reply}",
        reply_markup=markup,
    )


def slots_updated_for_student_message(
    parsed_slots_reply: str, markup: InlineKeyboardMarkup
):
    return BotMessage(
        text=f"{BotStrings.Student.SLOTS_UPDATED}\n\n{parsed_slots_reply}",
        reply_markup=markup,
    )


def slot_is_taken_message(student_username: str, slot_time: str) -> BotMessage:
    return BotMessage(
        text=BotStrings.Teacher.SLOT_IS_TAKEN.format(
            student=student_username,
            slot_time=slot_time,
        ),
        reply_markup=None,
    )


def success_slot_bind_message(
    teacher: str, slot_time: str, markup: InlineKeyboardMarkup
) -> BotMessage:
    return BotMessage(
        text=BotStrings.Student.SLOTS_ASSIGN_SUCCESS.format(
            teacher=teacher,
            slot_time=slot_time,
        ),
        reply_markup=markup,
    )


def specify_week_message(markup: InlineKeyboardMarkup) -> BotMessage:
    return BotMessage(text=BotStrings.Common.SPECIFY_WEEK, reply_markup=markup)
