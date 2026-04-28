from typing import Any

from pydantic import BaseModel

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



class MessageRecipient(BaseModel):
    chat_id: int


class ButtonData(BaseModel):
    text: str
    callback_data: str

    @classmethod
    def from_callback(cls, text: str, callback_data: str) -> "ButtonData":
        return cls(text=text, callback_data=callback_data)


class RowData(BaseModel):
    buttons: list[ButtonData]

    @classmethod
    def from_buttons(cls, *buttons: ButtonData) -> "RowData":
        return cls(buttons=list(buttons))

    @classmethod
    def from_callback(cls, *button_drafts: tuple[str, str]) -> "RowData":
        return cls(
            buttons=[ButtonData(text=text, callback_data=callback) for text, callback in button_drafts]
        )


class MarkupData(BaseModel):
    rows: list[RowData]

    @classmethod
    def from_rows(cls, *rows: RowData) -> "MarkupData":
        return cls(rows=list(rows))

    @classmethod
    def from_row_callbacks(cls, *row_data: list[tuple[str, str]]) -> "MarkupData":
        rows = [
            RowData.from_callback(*button_draft)
            for button_draft in row_data
        ]
        return cls(rows=rows)


class BotMessage(BaseModel):
    text: str
    markup: MarkupData | None = None
    parse_mode: str | None = None

    def to_aiogram_kwargs(self) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
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
    message: BotMessage
    recipients: list[MessageRecipient]
