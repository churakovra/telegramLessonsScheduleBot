from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup


class TelegramNotifier:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_message(self, chat_id: int, message: str, reply_markup: InlineKeyboardMarkup | None = None):
        await self.bot.send_message(
            chat_id=chat_id,
            text=message,
            reply_markup=reply_markup
        )
