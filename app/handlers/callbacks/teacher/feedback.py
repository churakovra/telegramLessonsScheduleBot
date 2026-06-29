from aiogram import Router
from aiogram.types import CallbackQuery

from app.keyboard.callback_factories.feedback import TeacherFeedbackListCallback
from app.keyboard.fabric import teacher_sub_menu_statistics
from app.message.models import BotMessage
from app.schemas.user import UserDTO
from app.services.container import Services
from app.services.feedback_service import FeedbackSummary
from app.utils.bot_strings import BotStrings
from app.utils.datetime_utils import full_format_no_sec
from app.utils.enums.bot_values import StatisticsPeriod

router = Router()


@router.callback_query(TeacherFeedbackListCallback.filter())
async def list_teacher_feedback(
    callback: CallbackQuery,
    services: Services,
    user: UserDTO,
) -> None:
    summary = await services.feedback.get_teacher_feedback(
        user.uuid,
        StatisticsPeriod.MONTH,
    )
    await callback.message.answer(
        **BotMessage(
            text=_format_feedback(summary),
            markup=teacher_sub_menu_statistics(),
        ).to_aiogram_kwargs()
    )
    await callback.answer()


def _format_feedback(summary: FeedbackSummary) -> str:
    if not summary.feedback:
        return BotStrings.Teacher.FEEDBACK_NOT_FOUND

    lines = [
        BotStrings.Teacher.FEEDBACK_LIST.format(average=summary.average_rating),
        "",
    ]
    for item in summary.feedback[:10]:
        comment = f" - {item.comment}" if item.comment else ""
        lines.append(
            f"{item.slot_time.strftime(full_format_no_sec)} "
            f"{item.student_name}: {item.rating}/5{comment}"
        )
    return "\n".join(lines)
