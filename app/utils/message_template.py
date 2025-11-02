from aiogram.types import InlineKeyboardMarkup

from app.schemas.bot_message import BotMessage
from app.utils.bot_strings import BotStrings


class MessageTemplate:
    @staticmethod
    def get_menu_message(username: str, markup: InlineKeyboardMarkup):
        return BotMessage(
            message_text=BotStrings.Common.MENU.format(user=username),
            reply_markup=markup,
        )

    @staticmethod
    def notify_teacher_new_slot(student: str, slot_time: str):
        return BotMessage(
            message_text=BotStrings.Teacher.SLOT_IS_TAKEN.format(
                student=student,
                slot_time=slot_time,
            ),
            reply_markup=None,
        )
