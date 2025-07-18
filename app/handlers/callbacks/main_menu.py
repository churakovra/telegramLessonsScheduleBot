from aiogram import Router
from aiogram.types import CallbackQuery

from app.utils.config.logger import setup_logger
from app.utils.keyboards.callback_factories.main_menu import MainMenuCallback
from app.utils.keyboards.sub_menu_markup import get_sub_menu_markup
from app.utils.bot_strings import BotStrings

router = Router()

logger = setup_logger()


@router.callback_query(MainMenuCallback.filter())
async def handle_callback(
        callback: CallbackQuery,
        callback_data: MainMenuCallback
):
    logger.debug("In cg-t callback handler")
    username = callback.from_user.username

    data = callback_data.menu_type
    logger.debug(f"callback data = {data}")
    markup = get_sub_menu_markup(data)

    await callback.message.answer(
        text=BotStrings.MENU.format(username),
        reply_markup=markup
    )
    await callback.message.delete()
    await callback.answer()
