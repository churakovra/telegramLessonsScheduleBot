from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.utils.enums.bot_values import KeyboardType
from app.utils.keyboard.context import KeyboardContext
from app.utils.logger import setup_logger

from ..keyboard import keyboard_registry


logger = setup_logger(__name__)



class MarkupBuilder:
    
    async def build(self, markup: KeyboardType, context: KeyboardContext) -> InlineKeyboardMarkup:
        keyboard_factory = keyboard_registry[markup]
        builder = InlineKeyboardBuilder()
        keyboard = keyboard_factory(builder, context)
        return keyboard.as_markup()
