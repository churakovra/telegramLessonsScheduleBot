from aiogram import Bot

class TelegramNotifier:
    def __init__(self, bot: Bot):
        self.bot = bot