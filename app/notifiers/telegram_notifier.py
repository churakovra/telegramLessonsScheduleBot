from aiogram import Bot

from app.schemas.bot_message import BotMessage


class TelegramNotifier:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.sent_messages: dict[int, list[BotMessage]] = dict()

    async def send_message(self, bot_message: BotMessage):
        self.add_message(bot_message)
        await self.bot.send_message(
            chat_id=bot_message.receiver_chat_id,
            text=bot_message.message_text,
            reply_markup=bot_message.reply_markup
        )

    def add_message(self, bot_message: BotMessage):
        try:
            self.sent_messages[bot_message.receiver_chat_id].append(bot_message)
        except KeyError:
            self.sent_messages[bot_message.receiver_chat_id] = list[BotMessage]()
            self.sent_messages[bot_message.receiver_chat_id].append(bot_message)

    def pop_message(self, chat_id) -> BotMessage:
        res = self.sent_messages[chat_id][len(self.sent_messages[chat_id]) - 1]
        self.sent_messages[chat_id].pop()
        return res
