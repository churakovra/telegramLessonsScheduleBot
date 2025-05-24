from app.models.BotMessage import BotMessage
from app.notifiers.telegram_notifier import TelegramNotifier


def pop_message_use_case(chat_id: int, notifier: TelegramNotifier) -> BotMessage:
    return notifier.pop_message(chat_id)