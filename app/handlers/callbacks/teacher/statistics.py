from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.keyboard.callback_factories.statistics import StatisticsPeriodCallback
from app.keyboard.fabric import teacher_sub_menu_statistics
from app.message.models import BotMessage
from app.schemas.user import UserDTO
from app.services.container import Services
from app.services.statistics_service import TeacherStats
from app.utils.bot_strings import BotStrings
from app.utils.enums.menu_type import MenuType

router = Router()


@router.callback_query(
    StatisticsPeriodCallback.filter(F.menu_type == MenuType.TEACHER)
)
async def show_teacher_statistics(
    callback: CallbackQuery,
    callback_data: StatisticsPeriodCallback,
    services: Services,
    user: UserDTO,
) -> None:
    stats = await services.statistics.get_teacher_stats(user.uuid, callback_data.period)
    await callback.message.answer(
        **BotMessage(
            text=_format_teacher_stats(stats),
            markup=teacher_sub_menu_statistics(),
        ).to_aiogram_kwargs()
    )
    await callback.answer()


def _format_teacher_stats(stats: TeacherStats) -> str:
    if stats.total_lessons == 0:
        return BotStrings.Teacher.STATISTICS_NOT_FOUND

    breakdown = "\n".join(
        f"{student}: {count}" for student, count in stats.lessons_per_student.items()
    )
    return "\n".join(
        [
            f"Занятий проведено: {stats.total_lessons}",
            f"Часов: {stats.total_hours}",
            f"Доход: {stats.total_earnings}",
            f"Популярный предмет: {stats.most_popular_lesson_type or '-'}",
            "",
            "По ученикам:",
            breakdown or "-",
        ]
    )
