from aiogram import Router
from aiogram.types import CallbackQuery

from app.keyboard.callback_factories.join_request import (
    TeacherJoinRequestDecisionCallback,
    TeacherJoinRequestListCallback,
)
from app.keyboard.fabric import (
    teacher_display_name,
    teacher_join_request_buttons,
    teacher_main_menu,
)
from app.message.models import BotMessage
from app.notifier.sender import MessageSender
from app.schemas.user import UserDTO
from app.services.container import Services
from app.utils.bot_strings import BotStrings

router = Router()


@router.callback_query(TeacherJoinRequestListCallback.filter())
async def list_join_requests(
    callback: CallbackQuery,
    services: Services,
    user: UserDTO,
) -> None:
    requests = await services.join_request.get_pending_for_teacher(user.uuid)
    if not requests:
        message = BotMessage(
            text=BotStrings.Teacher.JOIN_REQUESTS_NOT_FOUND,
            markup=teacher_main_menu(),
        )
    else:
        message = BotMessage(
            text=BotStrings.Teacher.JOIN_REQUESTS,
            markup=teacher_join_request_buttons(requests=requests),
        )
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()


@router.callback_query(TeacherJoinRequestDecisionCallback.filter())
async def decide_join_request(
    callback: CallbackQuery,
    callback_data: TeacherJoinRequestDecisionCallback,
    services: Services,
    user: UserDTO,
    sender: MessageSender,
) -> None:
    teacher = await services.teacher.get_teacher_by_uuid(user.uuid)
    if callback_data.approve:
        request = await services.join_request.approve(callback_data.request_uuid)
        student = await services.student.get_student_by_uuid(request.student_uuid)
        await sender.send_to_chat(
            chat_id=student.chat_id,
            text=BotStrings.Student.JOIN_REQUEST_APPROVED.format(
                teacher_name=teacher_display_name(teacher)
            ),
        )
        text = BotStrings.Teacher.JOIN_REQUEST_APPROVED
    else:
        request = await services.join_request.reject(callback_data.request_uuid)
        student = await services.student.get_student_by_uuid(request.student_uuid)
        await sender.send_to_chat(
            chat_id=student.chat_id,
            text=BotStrings.Student.JOIN_REQUEST_REJECTED,
        )
        text = BotStrings.Teacher.JOIN_REQUEST_REJECTED

    await callback.message.answer(
        **BotMessage(text=text, markup=teacher_main_menu()).to_aiogram_kwargs()
    )
    await callback.answer()
