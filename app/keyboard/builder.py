from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.utils.enums.bot_values import KeyboardType
from app.keyboard.context import KeyboardContext
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
        keyboard = keyboard_factory(builder, context)
        return keyboard.as_markup()

    # TODO Fix MarkupBuilder in handlers and test this shiet..