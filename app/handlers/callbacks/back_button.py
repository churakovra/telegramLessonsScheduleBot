from operator import call
from aiogram import Router
from aiogram.types import CallbackQuery

from app.utils.keyboards.callback_factories.back import BackCallback
from app.utils.keyboards.main_menu_markup import get_main_menu_markup
from app.services.user_service import UserService
from app.utils.enums.bot_values import UserRoles
from app.utils.exceptions.user_exceptions import UserNotFoundException, UserUnknownRoleException


from sqlalchemy.ext.asyncio import AsyncSession


router = Router()

@router.callback_query(BackCallback.filter())
async def handle_callback(
    callback: CallbackQuery,
    callback_data: BackCallback,
    session: AsyncSession
):
    parent_keyboard = callback_data.parent_keyboard
    if parent_keyboard != "menu_keyboard": # TODO Вынести в ENUM
        return
        
    username = callback.from_user.username
    try:
        user_service = UserService(session)
        user = await user_service.get_user(username)
        if user.is_admin:
            markup = get_main_menu_markup(UserRoles.ADMIN)
        elif user.is_teacher:
            markup = get_main_menu_markup(UserRoles.TEACHER)
        elif user.is_student:
            markup = get_main_menu_markup(UserRoles.STUDENT)
        else:
            raise UserUnknownRoleException(username, None)
        
        await callback.message.answer(text=callback.message.text, reply_markup=markup)
        await callback.message.delete()
        
    except (UserNotFoundException, UserUnknownRoleException) as e:
        await callback.message.answer(e.message)
        
    finally:
        await callback.answer()
