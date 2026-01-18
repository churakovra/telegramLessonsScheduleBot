from typing import TypedDict

from aiogram.types import InlineKeyboardMarkup


class BotMessage(TypedDict):
    text: str
    reply_markup: InlineKeyboardMarkup | None
