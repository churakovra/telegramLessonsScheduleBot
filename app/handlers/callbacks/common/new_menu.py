from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.keyboard import markup_type_by_role
from app.keyboard.builder import MarkupBuilder
from app.keyboard.callback_factories.menu import MenuCallback
from app.schemas.user_dto import UserDTO
from app.utils.enums.menu_type import MenuType
from app.utils.message_template import main_menu_message

router = Router()


@router.callback_query(MenuCallback.filter(F.menu_type == MenuType.NEW))
async def handle_callback(
    callback: CallbackQuery, callback_data: MenuCallback, user: UserDTO
):
    markup = MarkupBuilder.build(markup_type_by_role[user.role])
    bot_message = main_menu_message(markup)
    await callback.message.answer(**bot_message)
    await callback.answer()
