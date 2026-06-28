from aiogram import Router
from aiogram.types import CallbackQuery

from app.keyboard.callback_factories.admin import AdminDashboardCallback
from app.keyboard.fabric import admin_dashboard_menu
from app.message.models import BotMessage
from app.schemas.user import UserDTO
from app.services.container import Services
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import UserRole

router = Router()


@router.callback_query(AdminDashboardCallback.filter())
async def show_admin_dashboard(
    callback: CallbackQuery,
    services: Services,
    user: UserDTO,
) -> None:
    if user.role != UserRole.ADMIN:
        await callback.answer(BotStrings.Common.NOT_ENOUGH_RIGHTS, show_alert=True)
        return

    stats = await services.statistics.get_admin_stats()
    message = BotMessage(
        text=BotStrings.Admin.DASHBOARD.format(
            total_users=stats.total_users,
            total_teachers=stats.total_teachers,
            total_students=stats.total_students,
            total_lessons_this_week=stats.total_lessons_this_week,
            active_teachers_this_week=stats.active_teachers_this_week,
        ),
        markup=admin_dashboard_menu(),
    )
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()
