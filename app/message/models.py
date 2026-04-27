from typing import Any
from pydantic import BaseModel


class MessageRecipient(BaseModel):
    """Recipient for message delivery."""

    chat_id: int


class ButtonData(BaseModel):
    """Serializable button data."""

    text: str
    callback_data: str


class RowData(BaseModel):
    """Serializable row data."""

    buttons: list[ButtonData]


class MarkupData(BaseModel):
    """Serializable keyboard markup."""

    rows: list[RowData]


class BotMessage(BaseModel):
    """Serializable message model for AMQP transport.

    Replaces: AbstractBotMessageContext, MessagePack
    """

    text: str
    markup: MarkupData | None = None
    parse_mode: str | None = None

    def to_aiogram_kwargs(self) -> dict[str, Any]:
        """Convert to kwargs for aiogram Bot.send_message()."""
        from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
        from aiogram.utils.keyboard import InlineKeyboardBuilder

        kwargs = {
            "text": self.text,
            "parse_mode": self.parse_mode,
        }

        if self.markup:
            builder = InlineKeyboardBuilder()
            for row in self.markup.rows:
                buttons = [
                    InlineKeyboardButton(text=b.text, callback_data=b.callback_data)
                    for b in row.buttons
                ]
                builder.row(*buttons)
            kwargs["reply_markup"] = builder.as_markup()

        return kwargs


class MessageEnvelope(BaseModel):
    """Container for message + recipients. Sent via AMQP."""

    message: BotMessage
    recipients: list[MessageRecipient]
