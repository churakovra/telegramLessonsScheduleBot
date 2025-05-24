from dataclasses import dataclass

from aiogram.types import InlineKeyboardMarkup


@dataclass
class BotMessage:
    receiver_user_id: int
    receiver_username: str
    receiver_chat_id: int
    message_text: str
    reply_markup: InlineKeyboardMarkup | None = None