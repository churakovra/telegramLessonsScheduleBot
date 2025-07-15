from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.config.logger import setup_logger
from app.keyboards.sub_menu_markup import get_sub_menu_markup
from app.utils.bot_strings import BotStrings

router = Router()

logger = setup_logger()

@router.callback_query(F.data.startswith(BotStrings.CALLBACK_GROUP_TEACHER))
async def handle_callback(
        callback: CallbackQuery
):
    logger.debug("In cg-t callback handler")
    username = callback.from_user.username

    data = callback.data
    logger.debug(f"callback data = {data}")
    markup = get_sub_menu_markup(data)

    await callback.message.answer(
        text=BotStrings.MENU.format(username),
        reply_markup=markup
    )
    await callback.message.delete()
    await callback.answer()
