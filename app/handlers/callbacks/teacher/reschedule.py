from aiogram import Router
from aiogram.types import CallbackQuery

from app.keyboard.callback_factories.reschedule import (
    TeacherRescheduleDecisionCallback,
    TeacherRescheduleListCallback,
)
from app.keyboard.fabric import teacher_reschedule_buttons, teacher_reschedule_menu
from app.message.models import BotMessage
from app.notifier.sender import MessageSender
from app.schemas.user import UserDTO
from app.services.container import Services
from app.utils.bot_strings import BotStrings

router = Router()


@router.callback_query(TeacherRescheduleListCallback.filter())
async def list_reschedule_requests(
    callback: CallbackQuery,
    services: Services,
    user: UserDTO,
) -> None:
    requests = await services.reschedule.get_pending_for_teacher(user.uuid)
    if not requests:
        message = BotMessage(
            text=BotStrings.Teacher.RESCHEDULE_REQUESTS_NOT_FOUND,
            markup=teacher_reschedule_menu(),
        )
    else:
        message = BotMessage(
            text=BotStrings.Teacher.RESCHEDULE_REQUESTS,
            markup=teacher_reschedule_buttons(requests=requests),
        )
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()


@router.callback_query(TeacherRescheduleDecisionCallback.filter())
async def decide_reschedule_request(
    callback: CallbackQuery,
    callback_data: TeacherRescheduleDecisionCallback,
    services: Services,
    sender: MessageSender,
) -> None:
    if callback_data.approve:
        request = await services.reschedule.approve_request(callback_data.uuid)
        student = await services.student.get_student_by_uuid(request.student_uuid)
        new_time = f"{request.requested_date:%d.%m.%Y} {request.requested_time:%H:%M}"
        await sender.send_to_chat(
            chat_id=student.chat_id,
            text=BotStrings.Student.RESCHEDULE_APPROVED.format(new_time=new_time),
        )
        text = BotStrings.Teacher.RESCHEDULE_APPROVED.format(new_time=new_time)
    else:
        request = await services.reschedule.reject_request(callback_data.uuid)
        student = await services.student.get_student_by_uuid(request.student_uuid)
        await sender.send_to_chat(
            chat_id=student.chat_id,
            text=BotStrings.Student.RESCHEDULE_REJECTED,
        )
        text = BotStrings.Teacher.RESCHEDULE_REJECTED

    await callback.message.answer(
        **BotMessage(text=text, markup=teacher_reschedule_menu()).to_aiogram_kwargs()
    )
    await callback.answer()
