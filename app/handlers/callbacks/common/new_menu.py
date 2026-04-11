from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.keyboard.callback_factories.menu import MenuCallback
from app.keyboard.fabric import admin_main_menu, student_main_menu, teacher_main_menu
from app.message.models import BotMessage
from app.schemas.user import UserDTO
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import UserRole
from app.utils.enums.menu_type import MenuType

router = Router()


@router.callback_query(MenuCallback.filter(F.menu_type == MenuType.NEW))
async def handle_callback(
    callback: CallbackQuery, user: UserDTO
):
    # Get appropriate main menu markup based on user role
    if user.role == UserRole.TEACHER:
        markup = teacher_main_menu()
    elif user.role == UserRole.STUDENT:
        markup = student_main_menu()
    elif user.role == UserRole.ADMIN:
        markup = admin_main_menu()
    else:
        markup = None
    
    message = BotMessage(text=BotStrings.Common.GREETING.format(user=user.username), markup=markup)
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()
