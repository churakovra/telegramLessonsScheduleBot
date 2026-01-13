from aiogram import Bot

from app.schemas.bot_message import BotMessage
from app.schemas.user_dto import UserDTO


class TelegramNotifier:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_message(self, bot_message: BotMessage, receiver_chat_id):
        await self.bot.send_message(chat_id=receiver_chat_id, **bot_message)

    async def send_message_to_users(
        self, bot_message: BotMessage, users: list[UserDTO]
    ):
        for user in users:
            await self.send_message(bot_message, user.chat_id)
