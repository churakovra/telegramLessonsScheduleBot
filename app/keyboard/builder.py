from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.keyboard.context import KeyboardContext
from app.utils.enums.bot_values import KeyboardType
from app.utils.logger import setup_logger

from ..keyboard import keyboard_registry

logger = setup_logger(__name__)


class MarkupBuilder:
    @staticmethod
    def build(
        keyboard_type: KeyboardType, context: KeyboardContext | None = None
    ) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        keyboard_factory = keyboard_registry[keyboard_type]
        buttons, adjust = keyboard_factory(context)
        for button_text, callback in buttons:
            builder.button(text=button_text, callback_data=callback)
        builder.adjust(adjust)
        return builder.as_markup()

    # TODO Fix MarkupBuilder in handlers and test this shiet..
