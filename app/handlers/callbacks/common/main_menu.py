from aiogram import Router
from aiogram.types import CallbackQuery

from app.utils.logger import setup_logger
from app.utils.keyboards.callback_factories.menu import MainMenu
from app.utils.keyboards.markup_builder import MarkupBuilder


router = Router()

logger = setup_logger(__name__)


@router.callback_query(MainMenu.filter())
async def handle_callback(callback: CallbackQuery, callback_data: MainMenu):

    data = callback_data.menu_type
    markup = MarkupBuilder.sub_menu_markup(data)

    await callback.message.answer(text=callback.message.text, reply_markup=markup)
    await callback.message.delete()
    await callback.answer()
