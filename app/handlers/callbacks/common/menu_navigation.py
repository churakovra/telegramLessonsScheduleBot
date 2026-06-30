from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.keyboard.callback_factories.menu import MenuCallback
from app.keyboard.fabric import (
    admin_main_menu,
    admin_sub_menu_temp,
    get_main_menu_by_role,
    student_main_menu,
    student_sub_menu_slot,
    student_sub_menu_statistics,
    teacher_main_menu,
    teacher_recurrence_menu,
    teacher_reschedule_menu,
    teacher_sub_menu_lesson,
    teacher_sub_menu_notification,
    teacher_sub_menu_slot,
    teacher_sub_menu_statistics,
    teacher_sub_menu_student,
)
from app.message.models import BotMessage
from app.schemas.user import UserDTO
from app.utils.bot_strings import BotStrings
from app.utils.enums.menu_type import MenuType
from app.utils.logger import setup_logger

router = Router()

logger = setup_logger(__name__)


markup_type_by_menu_type = {
    MenuType.TEACHER: teacher_main_menu,
    MenuType.STUDENT: student_main_menu,
    MenuType.ADMIN: admin_main_menu,
    MenuType.TEACHER_STUDENT: teacher_sub_menu_student,
    MenuType.TEACHER_SLOT: teacher_sub_menu_slot,
    MenuType.TEACHER_LESSON: teacher_sub_menu_lesson,
    MenuType.TEACHER_NOTIFICATION: teacher_sub_menu_notification,
    MenuType.TEACHER_STATISTICS: teacher_sub_menu_statistics,
    MenuType.TEACHER_RECURRENCE: teacher_recurrence_menu,
    MenuType.TEACHER_RESCHEDULE: teacher_reschedule_menu,
    MenuType.STUDENT_SLOT: student_sub_menu_slot,
    MenuType.STUDENT_STATISTICS: student_sub_menu_statistics,
    MenuType.ADMIN_TEMP: admin_sub_menu_temp,
}

main_menus = [MenuType.TEACHER, MenuType.STUDENT, MenuType.ADMIN]


@router.callback_query(MenuCallback.filter(F.menu_type.in_(markup_type_by_menu_type)))
async def handle_menu_navigation(
    callback: CallbackQuery,
    callback_data: MenuCallback,
    user: UserDTO,
) -> None:
    menu_type = callback_data.menu_type
    message_text = (
        BotStrings.Common.MENU
        if menu_type in main_menus
        else BotStrings.Common.SUB_MENU
    )

    # Get markup from fabric function
    fabric_func = markup_type_by_menu_type[menu_type]
    markup = fabric_func()

    message = BotMessage(text=message_text, markup=markup)
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()


@router.callback_query(MenuCallback.filter(F.menu_type == MenuType.CANCEL))
async def handle_cancel(
    callback: CallbackQuery,
    state: FSMContext,
    user: UserDTO,
):
    markup = get_main_menu_by_role(user.role)

    message = BotMessage(text=BotStrings.Common.MENU, markup=markup)
    await state.clear()
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()


@router.callback_query(MenuCallback.filter(F.menu_type == MenuType.NEW))
async def handle_callback(callback: CallbackQuery, user: UserDTO):
    markup = get_main_menu_by_role(user.role)

    message = BotMessage(
        text=BotStrings.Common.GREETING.format(user=user.username), markup=markup
    )
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()
