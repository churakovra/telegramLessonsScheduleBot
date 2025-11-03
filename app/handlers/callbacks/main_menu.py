from aiogram import Router
from aiogram.types import CallbackQuery

from app.config.logger import setup_logger
from app.utils.keyboards.callback_factories.main_menu import MainMenuCallback
from app.utils.keyboards.sub_menu_markup import get_sub_menu_markup

router = Router()

logger = setup_logger()


@router.callback_query(MainMenuCallback.filter())
async def handle_callback(callback: CallbackQuery, callback_data: MainMenuCallback):
    logger.debug("In cg-t callback handler")

    data = callback_data.menu_type
    logger.debug(f"callback data = {data}")
    markup = get_sub_menu_markup(data)

    await callback.message.answer(text=callback.message.text, reply_markup=markup)
    await callback.message.delete()
    await callback.answer()
