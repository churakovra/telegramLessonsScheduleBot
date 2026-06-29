from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.keyboard.callback_factories.statistics import StatisticsPeriodCallback
from app.keyboard.fabric import student_sub_menu_statistics
from app.message.models import BotMessage
from app.schemas.user import UserDTO
from app.services.container import Services
from app.services.statistics_service import StudentStats
from app.utils.bot_strings import BotStrings
from app.utils.enums.menu_type import MenuType

router = Router()


@router.callback_query(
    StatisticsPeriodCallback.filter(F.menu_type == MenuType.STUDENT)
)
async def show_student_statistics(
    callback: CallbackQuery,
    callback_data: StatisticsPeriodCallback,
    services: Services,
    user: UserDTO,
) -> None:
    stats = await services.statistics.get_student_stats(user.uuid, callback_data.period)
    await callback.message.answer(
        **BotMessage(
            text=_format_student_stats(stats),
            markup=student_sub_menu_statistics(),
        ).to_aiogram_kwargs()
    )
    await callback.answer()


def _format_student_stats(stats: StudentStats) -> str:
    if stats.total_lessons == 0 and stats.upcoming_lessons_count == 0:
        return BotStrings.Student.STATISTICS_NOT_FOUND

    return "\n".join(
        [
            f"Занятий посещено: {stats.total_lessons}",
            f"Часов: {stats.total_hours}",
            f"Преподаватели: {', '.join(stats.teachers) or '-'}",
            f"Предстоящих занятий: {stats.upcoming_lessons_count}",
        ]
    )
