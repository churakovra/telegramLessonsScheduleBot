from aiogram import F, Router
from aiogram.types import CallbackQuery


from app.services.user_service import UserService
from app.utils.enums.bot_values import KeyboardType, UserRole
from app.utils.enums.menu_type import MenuType
from app.utils.exceptions.user_exceptions import UserNotFoundException
from app.utils.keyboard.builder import MarkupBuilder
from app.utils.keyboard.callback_factories.menu import MenuCallback
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.message_template import main_menu_message

router = Router()


markup_type_by_role = {
    UserRole.TEACHER: KeyboardType.TEACHER_MAIN,
    UserRole.STUDENT: KeyboardType.STUDENT_MAIN,
    UserRole.ADMIN: KeyboardType.ADMIN_MAIN,
}



@router.callback_query(MenuCallback.filter(F.menu_type==MenuType.NEW))
async def handle_callback(callback: CallbackQuery, callback_data: MenuCallback, session: AsyncSession):
    username = callback.from_user.username
    user_service = UserService(session)
    try:
        user = await user_service.get_user(username)
        markup = MarkupBuilder.build(markup_type_by_role[user.role])
        bot_message = main_menu_message(username, markup)
        await callback.message.answer(**bot_message)
    except(UserNotFoundException) as e:
        await callback.message.answer(e.message)
    finally:
        await callback.answer()