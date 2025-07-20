from dataclasses import dataclass

from aiogram.types import InlineKeyboardMarkup


@dataclass
class BotMessage:
    message_text: str
    reply_markup: InlineKeyboardMarkup
