from aiogram import Router
from aiogram.types import CallbackQuery

from app.utils.keyboard.callback_factories.menu import NewMainMenu
from app.utils.keyboard.builder import MarkupBuilder
from app.utils.message_template import MessageTemplate

router = Router()


@router.callback_query(NewMainMenu.filter())
async def handle_callback(callback: CallbackQuery, callback_data: NewMainMenu):
    markup = MarkupBuilder.main_menu_markup(callback_data.role)
    bot_message = MessageTemplate.main_menu_message(callback_data.username, markup)
    await callback.message.answer(bot_message.message_text, reply_markup=bot_message.reply_markup)
    await callback.answer()
