from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.message.models import BotMessage, MessageEnvelope, MessageRecipient
from app.keyboard import fabric
from app.notifier.producer import MessageProducer
from app.utils.enums.bot_values import UserRole
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.message(Command("produce"))
async def produce(message: Message, producer: MessageProducer):
    # Build message with fabric markup
    markup = fabric.student_main_menu()
    bot_message = BotMessage(text="Test message from producer", markup=markup)

    # Wrap and send
    envelope = MessageEnvelope(
        message=bot_message, recipients=[MessageRecipient(chat_id=320854517)]
    )
    await producer.produce(envelope)
    await message.answer("Success")
