from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboard import markup_type_by_role
from app.keyboard.builder import MarkupBuilder
from app.keyboard.callback_factories.menu import MenuCallback
from app.services.user_service import UserService
from app.utils.enums.menu_type import MenuType
from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.utils.message_template import main_menu_message

router = Router()


@router.callback_query(MenuCallback.filter(F.menu_type == MenuType.NEW))
async def handle_callback(
    callback: CallbackQuery, callback_data: MenuCallback, session: AsyncSession
):
    username = callback.from_user.username
    user_service = UserService(session)
    try:
        user = await user_service.get_user(username)
        markup = MarkupBuilder.build(markup_type_by_role[user.role])
        bot_message = main_menu_message(markup)
        await callback.message.answer(**bot_message)
    except UserNotFoundException as e:
        await callback.message.answer(e.message)
    finally:
        await callback.answer()
