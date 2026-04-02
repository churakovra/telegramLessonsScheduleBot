from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.keyboard.callback_factories.menu import MenuCallback
from app.message.message import BotMessage
from app.schemas.user import UserDTO
from app.utils.enums.menu_type import MenuType

router = Router()


@router.callback_query(MenuCallback.filter(F.menu_type == MenuType.NEW))
async def handle_callback(
    callback: CallbackQuery, user: UserDTO
):
    message = BotMessage.main_menu(user.role)
    await callback.message.answer(**message.prepare())
    await callback.answer()
