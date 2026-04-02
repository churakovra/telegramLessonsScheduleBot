import logging

from pydantic import BaseModel

from app.message.context import AbstractBotMessageContext

logger = logging.getLogger(__name__)


class MessageRecipient(BaseModel):
    chat_id: int


class MessagePack(BaseModel):
    message_context: AbstractBotMessageContext
    message_recipients: list[MessageRecipient]
