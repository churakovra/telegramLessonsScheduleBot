from dataclasses import dataclass

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


@dataclass
class MarkupButton:
    text: str
    callback: str


@dataclass
class MarkupRow:
    buttons: list[MarkupButton]


@dataclass
class BotMarkup:
    rows: list[MarkupRow]

    def build(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for row in self.rows:
            buttons: list[InlineKeyboardButton] = []
            for button in row.buttons:
                buttons.append(
                    InlineKeyboardButton(
                        text=button.text, callback_data=button.callback
                    )
                )
            builder.row(*buttons)
        return builder.as_markup()
