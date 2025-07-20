from aiogram.types import InlineKeyboardMarkup

from app.schemas.bot_message import BotMessage
from app.utils.bot_strings import BotStrings


class MessageTemplate:
    @staticmethod
    def get_menu_message(username: str, markup: InlineKeyboardMarkup):
        return BotMessage(
            message_text=BotStrings.MENU.format(username, markup),
            reply_markup=markup
        )